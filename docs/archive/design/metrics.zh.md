# 使用 Kepler 监控容器功耗

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

Kepler Exporter 以 Prometheus 友好的格式公开在 Kubernetes 集群中运行的应用程序的统计信息，该格式可以被任何理解此格式的数据库抓取，例如 [Prometheus][0] 和 [Sysdig][1]。

Kepler 向 Prometheus 导出各种容器指标，其中主要的指标是与能耗相关的指标。

## Kepler 指标概述

所有特定于 Kepler Exporter 的指标都以 `kepler` 为前缀。

## 容器能耗的 Kepler 指标

- **kepler_container_joules_total** (Counter)

    此指标是给定容器的 CPU、dram、gpus 和其他主机组件的聚合封装/插槽能耗。
    每个组件都有单独的指标，将在本文档的下一部分详细介绍。

    出于性能原因，此指标简化了 Prometheus 指标。非常大的 promQL 查询通常会给 Prometheus 带来非常高的开销。

- **kepler_container_core_joules_total** (Counter)

    这测量某个容器使用的 CPU 内核的总能耗。
    通常，当系统可以访问 [RAPL][3] 指标时，此指标将反映 RAPL 功率计划 0 (PP0) 的比例容器能耗，即插槽中所有 CPU 内核消耗的能量。
    但是，此指标是处理器型号特定的，在某些服务器 CPU 上可能不可用。
    在所有支持 RAPL 的处理器上都可用的 RAPL CPU 指标是封装，我们将在另一个指标中详细说明。

    在某些情况下，RAPL 可用但内核指标不可用时，Kepler 可能使用能耗封装。
    但请注意，封装能耗不仅来自 CPU 内核，它是所有插槽能耗。

    如果 [RAPL][3] 不可用，Kepler 可能使用模型服务器估算此指标。

- **kepler_container_dram_joules_total** (Counter)

    此指标描述容器在 DRAM 中花费的总能量。

- **kepler_container_uncore_joules_total** (Counter)

    这测量某些非内核组件消耗的累积能量，这些组件通常是最后级缓存、集成 GPU 和内存控制器，但组件数量可能因系统而异。
    非内核指标是处理器型号特定的，在某些服务器 CPU 上可能不可用。

    当 [RAPL][3] 不可用时，如果节点 CPU 支持非内核指标，Kepler 可以使用模型服务器估算此指标。

- **kepler_container_package_joules_total** (Counter)

    这测量 CPU 插槽消耗的累积能量，包括所有内核和非内核组件（例如最后级缓存、集成 GPU 和内存控制器）。
    RAPL 封装能量通常是 PP0 + PP1，但 PP1 计数器可能会也可能不会考虑非内核组件的所有能量使用。
    因此，封装能耗可能高于内核 + 非内核。

    当 [RAPL][3] 不可用时，Kepler 可能使用模型服务器估算此指标。

- **kepler_container_other_joules_total** (Counter)

    这测量除 CPU 和 DRAM 之外的其他主机组件的累积能耗。
    绝大多数主板都有一个能耗传感器，可以通过内核 acpi 或 ipmi 访问。
    此传感器报告整个系统的能耗。
    此外，某些处理器架构支持 RAPL 平台域 (PSys)，它是"片上系统"(SOC) 消耗的能量。

    通常，此指标是主机能耗（来自 acpi）减去 RAPL 封装和 DRAM。

- **kepler_container_gpu_joules_total** (Counter)

    这测量某个容器使用的 GPU 的总能耗。
    目前，Kepler 仅支持 NVIDIA GPU，但此指标将来也会反映其他加速器。
    因此，当系统有 NVIDIA GPU 时，Kepler 可以通过 NVIDIA nvml 包使用 GPU 的进程能耗和利用率来计算容器的 gpu 能耗。

- **kepler_container_energy_stat** (Counter)

    此指标包含几个容器指标，标记有在模型服务器中用于预测的容器资源利用率 cgroup 指标。

    此指标是模型服务器特定的，可能随时更新。

## 容器资源利用率的 Kepler 指标

### 基础指标

- **kepler_container_bpf_cpu_time_us_total**

    这使用 BPF 跟踪测量容器使用的总 CPU 时间。这是一个最小公开的指标。

### 硬件计数器指标

- **kepler_container_cpu_cycles_total**

    这使用硬件计数器测量容器使用的总 CPU 周期。
    为了支持性能和资源利用率的细粒度分析，硬件计数器由于其粒度和精度而特别受欢迎。

    CPU 周期是与 CPU 频率直接相关的指标。
    在处理器以固定频率运行的系统上，CPU 周期和总 CPU 时间大致相等。
    在处理器以变化频率运行的系统上，CPU 周期和总 CPU 时间将有不同的值。

- **kepler_container_cpu_instructions_total**

    这使用硬件计数器测量容器使用的总 cpu 指令。

    CPU 指令是计算 CPU 利用率的事实上的指标。

- **kepler_container_cache_miss_total**

    这使用硬件计数器测量给定容器发生的总缓存失效。

    由于没有直接测量内存访问的事件计数器，最后级缓存失效的次数为内存访问次数提供了一个很好的代理。
    如果发生 LLC 读取失效，应该发生对主内存的读取访问（但请注意，在回写缓存策略下，LLC 写入失效不一定是这种情况）。

!!! note
    您可以通过 `expose-hardware-counter-metrics` Kepler 执行选项或 `EXPOSE_HW_COUNTER_METRICS` 环境值启用/禁用这些指标的公开。

### IRQ 指标

- **kepler_container_bpf_net_tx_irq_total**

    这使用 BPF 跟踪测量容器传输到网卡的总数据包。

- **kepler_container_bpf_net_rx_irq_total**

    这使用 BPF 跟踪测量容器从网卡接收的总数据包。

- **kepler_container_bpf_block_irq_total**

    这使用 BPF 跟踪测量容器调用的块 I/O。

!!! note
    您可以通过 `EXPOSE_IRQ_COUNTER_METRICS` 环境值启用/禁用这些指标的公开。

## 节点信息的 Kepler 指标

- **kepler_node_info** (Counter)

    此指标显示节点元数据，如节点 CPU 架构。

## 节点能耗的 Kepler 指标

- **kepler_node_core_joules_total** (Counter)

    类似于容器指标，但表示在节点和操作系统上运行的所有容器的聚合（即"system_process"）。

- **kepler_node_uncore_joules_total** (Counter)

    类似于容器指标，但表示在节点和操作系统上运行的所有容器的聚合（即"system_process"）。

- **kepler_node_dram_joules_total** (Counter)

    类似于容器指标，但表示在节点和操作系统上运行的所有容器的聚合（即"system_process"）。

- **kepler_node_package_joules_total** (Counter)

    类似于容器指标，但表示在节点和操作系统上运行的所有容器的聚合（即"system_process"）。

- **kepler_node_other_joules_total** (Counter)

    类似于容器指标，但表示在节点和操作系统上运行的所有容器的聚合（即"system_process"）。

- **kepler_node_gpu_joules_total** (Counter)

    类似于容器指标，但表示在节点和操作系统上运行的所有容器的聚合（即"system_process"）。

- **kepler_node_platform_joules_total** (Counter)

    此指标表示主机的总能耗。

    绝大多数主板都有一个能耗传感器，可以通过 acpi 或 ipmi 内核访问。
    此传感器报告整个系统的能耗。
    此外，某些处理器架构支持 RAPL 平台域 (PSys)，它是"片上系统"(SOC) 消耗的能量。

    通常，此指标是来自 Redfish BMC 或 acpi 的主机能耗。

- **kepler_node_energy_stat** (Counter)

    此指标包含来自节点的多个指标，标记有在模型服务器中使用的容器资源利用率 cgroup 指标。

    此指标是模型服务器特定的，可以随时更新。

!!! note
    "system_process" 是一个特殊指示符，将所有非容器工作负载聚合到系统进程消耗指标中。

## 节点资源利用率的 Kepler 指标

### 加速器指标

- **kepler_node_accelerator_intel_qat**

    这测量某个节点上加速器 Intel QAT 的利用率。当系统有 Intel QAT 时，Kepler 可以通过遥测计算节点 QAT 的利用率。

## 通过 Prometheus 表达式探索节点导出器指标

所有能耗指标都被定义为计数器，遵循 [Prometheus 指标指南](https://prometheus.io/docs/practices/naming/) 的能源相关指标。

焦耳的 `rate()` 给出以瓦特为单位的功率，因为速率函数返回每秒平均值。
因此，要获取容器能耗，您可以使用以下查询：

```go
sum by (pod_name, container_name, container_namespace, node)(irate(kepler_container_joules_total{}[1m]))
```

请注意，我们在容器指标中报告节点标签，因为操作系统指标"system_process"在所有节点上都具有相同的名称和命名空间，我们不希望聚合它们。

## RAPL 功率域

[RAPL 功率域支持](https://zhenkai-zhang.github.io/papers/rapl.pdf)在一些最近的 Intel 微架构中（消费级/服务器级）：

| 微架构 | Package | CORE (PP0) | UNCORE (PP1) | DRAM |
|---|---|---|---|---|
|      Haswell      |   Y/Y   |   Y/**N**  |    Y/**N**   |  Y/Y |
|     Broadwell     |   Y/Y   |   Y/**N**  |    Y/**N**   |  Y/Y |
|     Skylake      |   Y/Y   |     Y/Y    |    Y/**N**   |  Y/Y |
|     Kaby Lake     |   Y/Y   |     Y/Y    |    Y/**N**   |  Y/Y |

[0]: <https://prometheus.io>
[1]:<https://sysdig.com/>
[3]:<https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/advisory-guidance/running-average-power-limit-energy-reporting.html>
