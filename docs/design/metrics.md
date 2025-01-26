# Monitoring Container Power Consumption with Kepler

Kepler Exporter exposes statistics from an application running in a Kubernetes cluster in a Prometheus-friendly format that can be
scraped by any database that understands this format, such as [Prometheus][0] and [Sysdig][1].

Kepler exports a variety of container metrics to Prometheus, where the main ones are those related
to energy consumption.

## Kepler Metrics Overview

All the metrics specific to the Kepler Exporter are prefixed with `kepler`.

## Kepler Metrics for Container Energy Consumption

- **kepler_container_joules_total** (Counter)

    This metric is the aggregated package/socket energy consumption of CPU, dram, gpus, and other host components for a given container.
    Each component has individual metrics which are detailed next in this document.

    This metric simplifies the Prometheus metric for performance reasons. A very large promQL query typically introduces a
    very high overhead on Prometheus.

- **kepler_container_core_joules_total** (Counter)

    This measures the total energy consumption on CPU cores that  a certain container has used.
    Generally, when the system has access to [RAPL][3] metrics, this metric will reflect the proportional container energy
    consumption of the RAPL Power Plan 0 (PP0), which is the energy consumed by all CPU cores in the socket.
    However, this metric is processor model specific and may not be available on some server CPUs.
    The RAPL CPU metric that is available on all processors that support RAPL is the package, which we will detail
    on another metric.

    In some cases where RAPL is available but core metrics are not, Kepler may use the energy consumption package.
    But note that package energy consumption is not just from CPU cores, it is all socket energy consumption.

    In case [RAPL][3] is not available, Kepler might estimate this metric using the model server.

- **kepler_container_dram_joules_total** (Counter)

    This metric describes the total energy spent in DRAM by a container.

- **kepler_container_uncore_joules_total** (Counter)

    This measures the cumulative energy consumed by certain uncore components, which are typically the last level cache,
    integrated GPU and memory controller, but the number of components may vary depending on the system.
    The uncore metric is processor model specific and may not be available on some server CPUs.

    When [RAPL][3] is not available, Kepler can estimate this metric using the model server if the node CPU supports the uncore metric.

- **kepler_container_package_joules_total** (Counter)

    This measures the cumulative energy consumed by the CPU socket, including all cores and uncore components (e.g.
    last-level cache, integrated GPU and memory controller).
    RAPL package energy is typically the PP0 + PP1, but PP1 counter may or may not account for all energy usage
    by uncore components. Therefore, package energy consumption may be higher than core + uncore.

    When [RAPL][3] is not available, Kepler might estimate this metric using the model server.

- **kepler_container_other_joules_total** (Counter)

    This measures the cumulative energy consumption on other host components besides the CPU and DRAM.
    The vast majority of motherboards have an energy consumption sensor that can be accessed via the kernel acpi or ipmi.
    This sensor reports the energy consumption of the entire system.
    In addition, some processor architectures support the RAPL platform domain (PSys) which is the energy consumed by the
    "System on a chipt" (SOC).

    Generally, this metric is the host energy consumption (from acpi) less the RAPL Package and DRAM.

- **kepler_container_gpu_joules_total** (Counter)

    This measures the total energy consumption on the GPUs that  a certain container has used.
    Currently, Kepler only supports NVIDIA GPUs, but this metric will also reflect other accelerators in the future.
    So when the system has NVIDIA GPUs, Kepler can calculate the energy consumption of the container's gpu using the GPU's
    processes energy consumption and utilization via NVIDIA nvml package.

- **kepler_container_energy_stat** (Counter)

    This metric contains several container metrics labeled with container resource utilization cgroup metrics
    that are used in the model server for predictions.

    This metric is specific for the model server and might be updated any time.

## Kepler Metrics for Container Resource Utilization

### Base Metric

- **kepler_container_bpf_cpu_time_us_total**

    This measures the total CPU time used by the container using BPF tracing. This is a minimum exposed metric.

### Hardware Counter Metrics

- **kepler_container_cpu_cycles_total**

    This measures the total CPU cycles used by the container using hardware counters.
    To support fine-grained analysis of performance and resource utilization, hardware counters are particularly desirable
    due to its granularity and precision..

    The CPU cycles is a metric directly related to CPU frequency.
    On systems where processors run at a fixed frequency, CPU cycles and total CPU time are roughly equivalent.
    On systems where processors run at varying frequencies, CPU cycles and total CPU time will have different values.

- **kepler_container_cpu_instructions_total**

    This measure the total cpu instructions used by the container using hardware counters.

    CPU instructions are the de facto metric for accounting for CPU utilization.

- **kepler_container_cache_miss_total**

    This measures the total cache miss that has occurred for a given container using hardware counters.

    As there is no event counter that measures memory access directly, the number of last-level cache misses gives
    a good proxy for the memory access number. If an LLC read miss occurs, a read access to main memory
    should occur (but note that this is not necessarily the case for LLC write misses under a write-back cache policy).

!!! note
    You can enable/disable expose of those metrics through `expose-hardware-counter-metrics` Kepler execution option or `EXPOSE_HW_COUNTER_METRICS` environment value.

### IRQ Metrics

- **kepler_container_bpf_net_tx_irq_total**

    This measures the total transmitted packets to network cards of the container using BPF tracing.

- **kepler_container_bpf_net_rx_irq_total**

    This measures the total packets received from network cards of the container using BPF tracing.

- **kepler_container_bpf_block_irq_total**

    This measures block I/O called of the container using BPF tracing.

!!! note
    You can enable/disable expose of those metrics through `EXPOSE_IRQ_COUNTER_METRICS` environment value.

## Kepler Metrics for Node Information

- **kepler_node_info** (Counter)

    This metric shows the node metadata like the node CPU architecture.

## Kepler Metrics for Node Energy Consumption

- **kepler_node_core_joules_total** (Counter)

    Similar to container metrics, but representing the aggregation of all containers running on the node and operating system (i.e. "system_process").

- **kepler_node_uncore_joules_total** (Counter)

    Similar to container metrics, but representing the aggregation of all containers running on the node and operating system (i.e. "system_process").

- **kepler_node_dram_joules_total** (Counter)

    Similar to container metrics, but representing the aggregation of all containers running on the node and operating system (i.e. "system_process").

- **kepler_node_package_joules_total** (Counter)

    Similar to container metrics, but representing the aggregation of all containers running on the node and operating system (i.e. "system_process").

- **kepler_node_other_joules_total** (Counter)

    Similar to container metrics, but representing the aggregation of all containers running on the node and operating system (i.e. "system_process").

- **kepler_node_gpu_joules_total** (Counter)

    Similar to container metrics, but representing the aggregation of all containers running on the node and operating system (i.e. "system_process").

- **kepler_node_platform_joules_total** (Counter)

    This metric represents the total energy consumption of the host.

    The vast majority of motherboards have a energy consumption sensor that can be accessed via the acpi or ipmi kernel.
    This sensor reports the energy consumption of the entire system.
    In addition, some processor architectures support the RAPL platform domain (PSys) which is the energy consumed by the
    "System on a chipt" (SOC).

    Generally, this metric is the host energy consumption from Redfish BMC or acpi.

- **kepler_node_energy_stat** (Counter)

    This metric contains multiple metrics from nodes labeled with container resource utilization cgroup metrics
    that are used in the model server.

    This metric is specific to the model server and can be updated at any time.

!!! note
    "system_process" is a special indicator that aggregate all the non-container workload into system process consumption metric.

## Kepler Metrics for Node Resource Utilization

### Accelerator Metrics

- **kepler_node_accelerator_intel_qat**

    This measures the utilization of the accelerator Intel QAT on a certain node. When the system has Intel QATs,
    Kepler can calculate the utilization of the node's QATs through telemetry.

## Exploring Node Exporter Metrics Through the Prometheus Expression

All the energy consumption metrics are defined as counter following the [Prometheus metrics guide](https://prometheus.io/docs/practices/naming/) for energy related metrics.

The `rate()` of joules gives the power in Watts since the rate function returns the average per second.
Therefore, for get the container energy consumption you can use the following query:

```go
sum by (pod_name, container_name, container_namespace, node)(irate(kepler_container_joules_total{}[1m]))
```

Note that we report the node label in the container metrics because the OS metrics "system_process" will have the
same name and namespace across all nodes and we do not want to aggregate them.

## RAPL Power Domain

[RAPL power domains supported](https://zhenkai-zhang.github.io/papers/rapl.pdf) in some
resent Intel microarchitecture (consumer-grade/server-grade):

| Microarchitecture | Package | CORE (PP0) | UNCORE (PP1) | DRAM |
|---|---|---|---|---|
|      Haswell      |   Y/Y   |   Y/**N**  |    Y/**N**   |  Y/Y |
|     Broadwell     |   Y/Y   |   Y/**N**  |    Y/**N**   |  Y/Y |
|      Skylake      |   Y/Y   |     Y/Y    |    Y/**N**   |  Y/Y |
|     Kaby Lake     |   Y/Y   |     Y/Y    |    Y/**N**   |  Y/Y |

[0]: <https://prometheus.io>
[1]:<https://sysdig.com/>
[3]:<https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/advisory-guidance/running-average-power-limit-energy-reporting.html>
