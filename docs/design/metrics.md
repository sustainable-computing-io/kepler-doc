# Monitoring Container Power Consumption with Kepler

Kepler Exporter exposes statistics from an application running in a Kubernetes cluster in a Prometheus-friendly format that can be
scraped by any database that understands this format, such as `Prometheus`_ and `Sysdig`_.

Kepler exports a variety of container metrics to Prometheus, where the main ones are those related 
to energy consumption. 


## Kepler metrics overview

All the metrics specific to the Kepler Exporter are prefixed with `kepler_`.


## Kepler metrics for Container Energy Consumption:

- **kepler_container_joules_total** (Counter)
    This metric is the aggregated package/socket energy consumption of CPU, dram, gpus, and other host components for a given container.
    Each component has individual metrics which are detailed next in this document.

    This metric simplifies the Prometheus metric for performance reasons. A very large promQL query typically introduces a
    very high overhead on Prometheus.

- **kepler_container_core_joules_total** (Counter)
    This measures the total energy consumption on CPU cores that  a certain container has used.
    Generally, when the system has access to `RAPL`_ metrics, this metric will reflect the porportinal container energy consumption of the RAPL
    Power Plan 0 (PP0), which is the energy consumed by all CPU cores in the socket.
    However, this metric is processor model specific and may not be available on some server CPUs.
    The RAPL CPU metric that is available on all processors that support RAPL is the package, which we will detail
    on another metric.

    In some cases where RAPL is available but core metrics are not, Kepler may use the energy consumption package.
    But note that package energy consumption is not just from CPU cores, it is all socket energy consumption.

    In case `RAPL`_ is not available, kepler might estimate this metric using the model server.

- **kepler_container_uncore_joules_total** (Counter)
    This measures the cumulative energy consumed by certain uncore components, which are typically the last level cache,
    integrated GPU and memory controller, but the number of components may vary depending on the system.
    The uncore metric is processor model specific and may not be available on some server CPUs.

    When `RAPL`_ is not available, kepler can estimate this metric using the model server if the node CPU supports the uncore metric.

- **kepler_container_package_joules_total** (Counter)
    This measures the cumulative energy consumed by the CPU socket, including all cores and uncore components (e.g.
    last-level cache, integrated GPU and memory controller).
    RAPL package energy is typically the PP0 + PP1, but PP1 counter may or may not account for all energy usage
    by uncore components. Therefore, package energy consumption may be higher than core + uncore.

    When `RAPL`_ is not available, kepler might estimate this metric using the model server.

- **kepler_container_other_host_components_joules_total** (Counter)
    This measures the cumulative energy consumption on other host components besides the CPU and DRAM.
    The vast majority of moderboards have a energy consumption sensor that can be accessed via the kernel acpi or ipmi.
    This sensor reports the energy consumption of the entire system.
    In addition, some processor architectures support the RAPL platform domain (PSys) which is the energy consumed by the
    "System on a chipt" (SOC).

    Generally, this metric is the host energy consumption (from acpi) less the RAPL Package and DRAM.

- **kepler_container_gpu_joules_total** (Counter)
    This measures the total energy consumption on the GPUs that  a certain container has used.
      Currently, Kepler only supports NVIDIA GPUs, but this metric will also reflect other accelerators in the future.
      So when the system has NVIDIA GPUs, kepler can calculate the energy consumption of the container's gpu using the GPU's
      processeses energy consumption and utilization via NVIDIA nvml package.

- **kepler_container_energy_stat** (Counter)
    This metric contains several container metrics labeled with container resource utilization cgroup metrics
    that are used in the model server for predictions.

    This metric is specific for the model server and might be updated any time.

Note:
    "system_process" is a special indicator that aggregate all the non-container workload into system process consumption metric.

## Kepler metrics for Container resource utilization:

- **kepler_container_cpu_cycles_total** (Counter)
    This measures the total CPU cycles used by the container using hardware counters.
    To support fine-grained analysis of performance and resource utilization, hardware counters are particularly desirable
    due to its granularity and precision..

    The CPU cycles is a metric directly related to CPU frequency.
    On systems where processors run at a fixed frequency, CPU cycles and total CPU time are roughly equivalent.
    On systems where processors run at varying frequencies, CPU cycles and total CPU time will have different values.
    
- **kepler_container_cpu_instr_total** (Counter)
    This measure the total cpu instructions used by the container using hardware counters.

    CPU instructions are the de facto metric for accounting for CPU utilization.

- **kepler_container_cache_miss_total** (Counter)
    This measures the total cache miss that has occurred for a given container using hardware counters.

    As there is no event counter that measures memory access directly, the number of last-level cache misses gives
    a good proxy for the memory access number. If an LLC read miss occurs, a read access to main memory
    should occur (but note that this is not necessarily the case for LLC write misses under a write-back cache policy).

Note:
    You can enable/disable expose of those metrics through `expose-hardware-counter-metrics` kepler execution option.

## Kepler metrics for Node information:

- **kepler_node_nodeInfo** (Counter)
    This metric shows the node metada like the node CPU architecture.

    Note that this metrics is deprecated and might be updated to `kepler_node_info` in the next release.

## Kepler metrics for Node energy consumption:

- **kepler_node_core_joules_total** (Counter)
    Similar to container metrics, but representing the aggregation of all containers running on the node and operating system (i.e. "system_process").

- **kepler_node_uncore_joules_total** (Counter)
    Similar to container metrics, but representing the aggregation of all containers running on the node and operating system (i.e. "system_process").

- **kepler_node_dram_joules_total** (Counter)
    Similar to container metrics, but representing the aggregation of all containers running on the node and operating system (i.e. "system_process").

- **kepler_node_package_joules_total** (Counter)
    Similar to container metrics, but representing the aggregation of all containers running on the node and operating system (i.e. "system_process").

- **kepler_node_other_host_components_joules_total** (Counter)
    Similar to container metrics, but representing the aggregation of all containers running on the node and operating system (i.e. "system_process").

- **kepler_node_gpu_joules_total** (Counter)
    Similar to container metrics, but representing the aggregation of all containers running on the node and operating system (i.e. "system_process").

- **kepler_node_platform_joules_total** (Counter)
   This metric represents the total energy consumption of the host.

    The vast majority of moderboards have a energy consumption sensor that can be accessed via the acpi or ipmi kernel.
    This sensor reports the energy consumption of the entire system.
    In addition, some processor architectures support the RAPL platform domain (PSys) which is the energy consumed by the
    "System on a chipt" (SOC).

    Generally, this metric is the host energy consumption (from acpi).

- **kepler_node_energy_stat** (Counter)
    This metric contains multiple metrics from nodes labeled with container resource utilization cgroup metrics
    that are used in the model server.

    This metric is specific to the model server and can be updated at any time.

## Exploring Node Exporter metrics through the Prometheus expression

All the energy consumption metrics are defined as counter following the `Prometheus metrics guide <https://prometheus.io/docs/practices/naming/>`_ for energy related metrics.

The `rate()` of joules gives the power in Watts since the rate function returns the average per second.
Therefore, for get the container energy consumption you can use the following query:


`sum by (pod_name, container_name, container_namespace, node) (`
  `irate(kepler_container_joules_total{}[1m])`
`)`


Note that we report the node label in the container metrics because the OS metrics "system_process" will have the same name and namespace across all nodes and we do not want to aggregate them.

## RAPL power domain

`RAPL power domains supported <https://zhenkai-zhang.github.io/papers/rapl.pdf>`_ in some 
resent Intel microarchitecture (consumer-grade/server-grade):

| Microarchitecture | Package | CORE (PP0) | UNCORE (PP1) | DRAM |
|---|---|---|---|---|
|      Haswell      |   Y/Y   |   Y/**N**  |    Y/**N**   |  Y/Y |
|     Broadwell     |   Y/Y   |   Y/**N**  |    Y/**N**   |  Y/Y |
|      Skylake      |   Y/Y   |     Y/Y    |    Y/**N**   |  Y/Y |
|     Kaby Lake     |   Y/Y   |     Y/Y    |    Y/**N**   |  Y/Y |

.. _Prometheus: https://prometheus.io

.. _Sysdig: https://sysdig.com/

.. _RAPL: https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/advisory-guidance/running-average-power-limit-energy-reporting.html
