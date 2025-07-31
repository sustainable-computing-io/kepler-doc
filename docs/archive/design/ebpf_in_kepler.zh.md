# Kepler中的ebpf

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

## 背景

### 什么是ebpf?

eBPF是一项革命性的技术，起源于Linux内核，可以在操作系统内核等特权上下文中运行沙盒程序。它用于安全有效地扩展内核的功能，而无需更改内核源代码或加载内核模块。[1]

### 什么是kprobe?

KProbes是Linux内核的一种调试机制，也可用于监视生产系统内的事件。KProbes使您能够动态地闯入任何内核例程，并以无中断的方式收集调试和性能信息。您可以在几乎任何内核代码地址设置陷阱，指定在遇到断点时要调用的处理程序例程。[2]

#### 如何查看已经注册的kprobes?

```bash
sudo cat /sys/kernel/debug/kprobes/list
```

### CPU硬件事件监控

性能计数器是在如今大多数CPU上均已实现的一种特殊的硬件计数器。这些计数器在统计某些特殊类型的硬件事件： 例如执行命令，缓存失效，或分支预测错误的同时并不会降低内核或者程序执行速度。[4]

使用系统调用 `perf_event_open` [5], Linux系统允许设置硬件和软件性能的性能监视。它返回一个文件描述符来读取性能信息。
这个系统调用使用 `pid` 和 `cpuid` 作为参数. Kepler使用`pid == -1`和`cpuid`作为实际的cpuid。
这种pid和cpu的组合允许测量指定cpu上的所有进程/线程。

#### 如何检查Linux内核是否支持`perf_event_open`?

检查是否存在`/proc/sys/kernel/perf_event_paranoid`，以了解内核是否支持`perf_event_open`以及允许测量的内容

```bash
   The perf_event_paranoid file can be set to restrict
   access to the performance counters.

   2      allow only user-space measurements (default since Linux 4.6).
   1      allow both kernel and user measurements (default before Linux 4.6).
   0      allow access to CPU-specific data but not raw tracepoint samples.
  -1      no restrictions.


   Measuring all process/threads required CAP_SYS_ADMIN capability or a value less than 1 in above file
```

**CAP_SYS_ADMIN** 是最高级别的能力，它可能具有一些安全影响。

## kepler探测内核进程
kepler捕捉内核函数`finish_task_switch`[3], 该函数负责在任务切换发生后进行清理。由于探测通过`kprobe`发生，对它的调用发生在调用`finish_task_switch`之前，而不是在探测函数返回后调用`kretprobe`。

当内核发生上下文切换时，函数`finish_task_switch`在新进程进入CPU时被调用。这个函数接受参数类型`task_struct*`，该参数类型包含所有关于离开CPU进程的所有信息。[3]

kepler的探测函数

```c
int kprobe__finish_task_switch(struct pt_regs *ctx, struct task_struct *prev)
```

第一个参数的类型是指向`pt_regs`结构的指针，该结构指的是在内核函数条目时保持CPU寄存器状态的结构。此结构包含与CPU寄存器相对应的字段，例如通用寄存器（例如，r0、r1等）、堆栈指针（sp）、程序计数器（pc）和其他特定于体系结构的寄存器。
第二个参数是指向`task_struct`的指针，该指针包含前一任务的任务信息，即离开CPU的任务。

## Kepler监控CPU硬件事件

Kepler监控以下CPU硬件事件

| PERF Type          | Perf Count Type              | Description                                                                                                                                                                               | Array name <br>(in bpf program) |
|--------------------|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------|
| PERF_TYPE_HARDWARE | PERF_COUNT_HW_CPU_CYCLES     | Total CPU cycles; can get affected by CPU frequency scaling                                                                                                                               | cpu_cycles_hc_reader            |
| PERF_TYPE_HARDWARE | PERF_COUNT_HW_REF_CPU_CYCLES | Total CPU cycles; not affected by CPU frequency scaling                                                                                                                                   | cpu_ref_cycles_hc_reader        |
| PERF_TYPE_HARDWARE | PERF_COUNT_HW_INSTRUCTIONS   | Retired instructions.  Be careful, these can be affected by various issues, most notably hardware interrupt counts.                                                                       | cpu_instr_hc_reader             |
| PERF_TYPE_HARDWARE | PERF_COUNT_HW_CACHE_MISSES   | Cache misses. Usually this indicates Last Level Cache misses; this is intended to be used in conjunction with the PERF_COUNT_HW_CACHE_REFERENCES event to calculate cache miss rates. | cache_miss_hc_reader            |

性能计数器通过特殊的文件描述符进行访问。每个使用的虚拟计数器都有一个文件描述符。文件描述符与相应的数组相关联。当使用bcc包装器函数时，它读取相应的fd并返回值。

## 计算进程CPU运行总时间

ebpf函数(`bpfassets/perf_event/perf_event.c`)维护一个基于时间戳对于`<pid, cpuid>`表。时间戳表示在cpu上调度pid时为pid调用`kprobe_finish_task_switch`的时刻`<cpuid>`

```c
// <Task PID, CPUID> => Context Switch Start time

typedef struct pid_time_t { u32 pid; u32 cpu; } pid_time_t;
BPF_HASH(pid_time, pid_time_t);
// pid_time is the name of variable which if of type map
```
在函数`get_on_cpu_time`中，当前时间戳与`pid_time`映射中的时间戳之间的差用于计算当前cpu上先前任务的`on_cpu_time_delta`。

此`on_cpu_time_delta`用于累积前一任务的`process_run_time`度量。

## 计算进程CPU周期

对于进程的CPU周期，bpf程序维护`cpu_cycles`数组，并通过`cpuid`作为索引。这个数组包含性能数组`cpu_cycles_hc_reader`，是一个性能事件的数组。

在每个任务切换上，
- 从性能计数器阵列cpu_cycles_hc_reader读取当前值
- 检索cpucycles中的上一个值
- delta是通过从当前值减去之前的值来计算的
- 当前值被复制回cpucycles，用于下一个任务切换

由此计算出的增量是离开cpu的进程所使用的cpu周期。

## 计算进程参考CPU周期

与计算CPU周期的过程相同，所使用的性能数组的替换为`cpu_ref_cycles_hc_reader`，prev值存储在`CPU_ref_cycles`中

## 计算进程CPU指令

与计算CPU周期的过程相同，所使用的性能数组的替换为`cpu_instr_hc_reader`，prev值存储在`cpu_instr`中

## 计算进程缓存失效

与计算CPU周期的过程相同，所使用的性能数组的替换为`cache_miss_hc_reader`，prev值存储在`cache_miss`中

## 计算CPU上平均频率

```c
avg_freq = ((on_cpu_cycles_delta * CPU_REF_FREQ) / on_cpu_ref_cycles_delta) * HZ;

CPU_REF_FREQ = 2500
HZ = 1000
```

此值存储在数组`cpu_freq_array`中

## 进程表

bpf程序维护一个名为`processes`的bpf散列。此散列维护为进程计算的数据。Kepler从这个散列中读取值（在bcc中称为`Table`）并生成度量。

| Key | Value            |Description                                                                                               |
|-----|------------------|-----------------------------------------------------------------------------------------------|
| pid | cgroupid         | Process CGroupID                                                                              |
|     | pid              | Process ID                                                                                    |
|     | process_run_time | Total time a process occupies CPU (calculated each time process leaves CPU on context switch) |
|     | cpu_cycles       | Total CPU cycles consumed by process                                                          |
|     | cpu_instr        | Total CPU instructions consumed by process                                                    |
|     | cache_miss       | Total Cache miss by process                                                                   |
|     | vec_nr           | Total number of soft irq handles by process (max 10)                                          |
|     | comm             | Process name (max length 16)                                                                  |

此散列由`container_hc_collector.go`中的内核收集器读取，用于收集指标。

## 参考

 [1] [https://ebpf.io/what-is-ebpf/](https://ebpf.io/what-is-ebpf/) , [https://www.splunk.com/en_us/blog/learn/what-is-ebpf.html](https://www.splunk.com/en_us/blog/learn/what-is-ebpf.html) , [https://www.tigera.io/learn/guides/ebpf/](https://www.tigera.io/learn/guides/ebpf/)

 [2] [An introduction to KProbes](https://lwn.net/Articles/132196/) , [Kernel Probes (Kprobes)](https://docs.kernel.org/trace/kprobes.html)

 [3] [finish_task_switch - clean up after a task-switch](https://elixir.bootlin.com/linux/v6.4-rc7/source/kernel/sched/core.c#L5157)

 [4] [Performance Counters for Linux](https://elixir.bootlin.com/linux/latest/source/tools/perf/design.txt)

 [5] [perf_event_open(2) — Linux manual page](https://www.man7.org/linux/man-pages/man2/perf_event_open.2.html)
