```markdown
# eBPF 在 Kepler 中的应用

## 背景知识

### 什么是 eBPF？

eBPF 是一项革命性技术，起源于 Linux 内核，能在操作系统内核等特权上下文中运行沙箱程序。它无需修改内核源代码或加载内核模块，即可安全高效地扩展内核功能。[1]

### 什么是 kprobe？

KProbes 是 Linux 内核的调试机制，也可用于生产系统的事件监控。它允许动态拦截任意内核例程，非破坏性地收集调试和性能信息。您可以在几乎任何内核代码地址设置断点，并指定触发断点时调用的处理程序。[2]

#### 如何列出当前注册的所有 kprobe？

```bash
sudo cat /sys/kernel/debug/kprobes/list
```

### 硬件 CPU 事件监控

性能计数器是现代 CPU 上的特殊硬件寄存器，可统计特定类型的硬件事件（如执行指令数、缓存未命中次数、分支预测错误次数），且不会降低内核或应用性能。[4]

通过系统调用 `perf_event_open`[5]，Linux 支持设置硬件和软件性能监控。该调用返回用于读取性能信息的文件描述符，接收 `pid` 和 `cpuid` 参数。Kepler 使用 `pid == -1` 和实际 CPU ID 作为参数，这种组合可测量指定 CPU 上所有进程/线程。

#### 如何检查内核是否支持 `perf_event_open`？

检查 `/proc/sys/kernel/perf_event_paranoid` 文件是否存在，可确认内核支持情况及测量权限：

```bash
   perf_event_paranoid 文件用于限制性能计数器访问权限：

   2      仅允许用户空间测量（Linux 4.6 后默认值）
   1      允许内核和用户空间测量（Linux 4.6 前默认值）
   0      允许访问 CPU 特定数据，但不允许原始跟踪点样本
  -1      无限制

   测量所有进程/线程需具备 CAP_SYS_ADMIN 能力或该文件值小于 1
```

**CAP_SYS_ADMIN** 是最高级别的能力，存在一定安全风险

## Kepler 监控的内核例程

Kepler 在 `finish_task_switch` 内核函数[3]设置探针，该函数负责任务切换后的清理工作。由于采用 `kprobe` 方式，探针会在 `finish_task_switch` 被调用前触发（若使用 `kretprobe` 则会在函数返回后触发）。

当内核发生上下文切换时，`finish_task_switch` 会被即将使用 CPU 的新任务调用。该函数接收 `task_struct*` 类型参数，包含 relinquishing CPU 的任务信息。[3]

Kepler 的探针函数为：
```c
int kprobe__finish_task_switch(struct pt_regs *ctx, struct task_struct *prev)
```
首参数为 `pt_regs` 结构体指针，保存内核函数入口时的 CPU 寄存器状态；次参数为 `task_struct` 指针，包含 relinquishing CPU 的上一任务信息。

## Kepler 监控的硬件 CPU 事件

Kepler 监控以下硬件 CPU 事件：

| PERF 类型          | 性能计数类型              | 描述                                                                                                                                                                               | BPF 程序中的数组名          |
|--------------------|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------|
| PERF_TYPE_HARDWARE | PERF_COUNT_HW_CPU_CYCLES     | 总 CPU 周期数，受 CPU 频率缩放影响                                                                                                                                               | cpu_cycles_hc_reader      |
| PERF_TYPE_HARDWARE | PERF_COUNT_HW_REF_CPU_CYCLES | 总 CPU 周期数，不受 CPU 频率缩放影响                                                                                                                                             | cpu_ref_cycles_hc_reader  |
| PERF_TYPE_HARDWARE | PERF_COUNT_HW_INSTRUCTIONS   | 已执行指令数（注意可能受硬件中断等因素影响）                                                                                                                                     | cpu_instr_hc_reader       |
| PERF_TYPE_HARDWARE | PERF_COUNT_HW_CACHE_MISSES   | 缓存未命中数（通常指末级缓存未命中，需与 PERF_COUNT_HW_CACHE_REFERENCES 事件结合计算未命中率）                                                                               | cache_miss_hc_reader      |

性能计数器通过特殊文件描述符访问，每个虚拟计数器对应一个文件描述符。使用 bcc 包装函数时，会自动读取对应 fd 并返回值。

## 计算进程（任务）总 CPU 时间

eBPF 程序 (`bpfassets/bcc/bcc.c`) 维护从 `<pid, cpuid>` 对到时间戳的映射，记录任务在指定 CPU 上触发 `kprobe__finish_task_switch` 的时刻：

```c
// <任务 PID, CPUID> => 上下文切换开始时间
typedef struct pid_time_t { u32 pid; u32 cpu; } pid_time_t;
BPF_HASH(pid_time, pid_time_t); // pid_time 是类型为 map 的变量名
```

在 `get_on_cpu_time` 函数中，通过当前时间戳与 `pid_time` 映射中时间戳的差值，计算上一任务在当前 CPU 上的 `on_cpu_time_delta`，并累加到该任务的 `process_run_time` 指标。

## 计算任务 CPU 周期数

对于 CPU 周期统计，BPF 程序维护名为 `cpu_cycles` 的数组（按 `cpuid` 索引），存储来自 perf 事件数组 `cpu_cycles_hc_reader` 的值。每次任务切换时：
1. 从 `cpu_cycles_hc_reader` 读取当前值
2. 获取 `cpu_cycles` 中存储的上次值
3. 计算当前值与上次值的差值
4. 将当前值写回 `cpu_cycles` 供下次使用
所得差值即为 relinquishing CPU 的进程消耗的 CPU 周期数。

## 计算任务参考 CPU 周期数

计算逻辑与 CPU 周期数相同，区别在于使用 `cpu_ref_cycles_hc_reader` 数组和 `cpu_ref_cycles` 存储变量。

## 计算任务 CPU 指令数

计算逻辑与 CPU 周期数相同，区别在于使用 `cpu_instr_hc_reader` 数组和 `cpu_instr` 存储变量。

## 计算任务缓存未命中数

计算逻辑与 CPU 周期数相同，区别在于使用 `cache_miss_hc_reader` 数组和 `cache_miss` 存储变量。

## 计算 "CPU 平均频率"

```c
avg_freq = ((on_cpu_cycles_delta * CPU_REF_FREQ) / on_cpu_ref_cycles_delta) * HZ;
// 其中 CPU_REF_FREQ = 2500，HZ = 1000
```
结果存储在 `cpu_freq_array` 数组中。

## 计算 "页缓存命中"

Kepler 通过 `kprobe__set_page_dirty` 和 `kprobe__mark_page_accessed` 探针函数分别追踪写操作和读操作的页缓存命中情况。

## 进程表

BPF 程序维护名为 `processes` 的哈希表（在 bcc 中称为 `Table`），存储进程的统计指标。Kepler 读取该表生成监控指标：

| 键   | 值                | 描述                                                                                               |
|------|-------------------|---------------------------------------------------------------------------------------------------|
| pid  | cgroupid         | 进程 CGroup ID                                                                                   |
|      | pid              | 进程 ID                                                                                         |
|      | process_run_time | 进程占用 CPU 的总时间（每次上下文切换时计算）                                                   |
|      | cpu_cycles       | 进程消耗的总 CPU 周期数                                                                          |
|      | cpu_instr        | 进程执行的总指令数                                                                              |
|      | cache_miss       | 进程产生的总缓存未命中数                                                                        |
|      | page_cache_hit   | 进程的页缓存命中总数                                                                            |
|      | vec_nr           | 进程处理的软中断总数（最大 10）                                                                 |
|      | comm             | 进程名称（最长 16 字符）                                                                        |

内核收集器 (`container_hc_collector.go`) 会读取该哈希表进行指标收集。

## 参考文献

[1] [eBPF 官网](https://ebpf.io/what-is-ebpf/) | [Splunk 介绍](https://www.splunk.com/en_us/blog/learn/what-is-ebpf.html) | [Tigera 指南](https://www.tigera.io/learn/guides/ebpf/)  
[2] [KProbes 介绍](https://lwn.net/Articles/132196/) | [内核文档](https://docs.kernel.org/trace/kprobes.html)  
[3] [finish_task_switch 函数](https://elixir.bootlin.com/linux/v6.4-rc7/source/kernel/sched/core.c#L5157)  
[4] [Linux 性能计数器](https://elixir.bootlin.com/linux/latest/source/tools/perf/design.txt)  
[5] [perf_event_open 手册](https://www.man7.org/linux/man-pages/man2/perf_event_open.2.html)
```