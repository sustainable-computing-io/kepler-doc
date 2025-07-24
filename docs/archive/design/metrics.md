# Kepler Metrics

This document describes the metrics exported by Kepler for monitoring energy
consumption at various levels (node, container, process, VM, pod).

## Overview

Kepler exports metrics in Prometheus format that can be scraped by Prometheus
or other compatible monitoring systems. All metrics follow the Prometheus
naming conventions and are prefixed with `kepler_`.

### Metric Types

- **COUNTER**: A cumulative metric that only increases over time (e.g., total energy consumption)
- **GAUGE**: A metric that can increase and decrease (e.g., current power consumption)

### Zone-Based Organization

Kepler organizes energy metrics by zones, which correspond to different hardware components:

- **package**: CPU socket-level energy (includes cores and uncore components)
- **core**: CPU core-level energy (available on some processors)
- **uncore**: Uncore components (last-level cache, integrated GPU, memory controller)
- **dram**: Memory energy consumption

## Metrics Reference

### Node Metrics

These metrics provide energy and power information at the node level, representing the total consumption of the entire system.

#### kepler_node_cpu_joules_total

- **Type**: COUNTER
- **Description**: Total energy consumption of CPU at node level in joules
- **Labels**:
  - `zone`: Energy zone (package, core, uncore, dram)
  - `path`: Hardware sensor path
- **Constant Labels**:
  - `node_name`: Name of the node

#### kepler_node_cpu_watts

- **Type**: GAUGE
- **Description**: Current power consumption of CPU at node level in watts
- **Labels**:
  - `zone`: Energy zone (package, core, uncore, dram)
  - `path`: Hardware sensor path
- **Constant Labels**:
  - `node_name`: Name of the node

#### kepler_node_cpu_active_joules_total

- **Type**: COUNTER
- **Description**: Energy consumption of CPU in active state at node level in joules
- **Labels**:
  - `zone`: Energy zone (package, core, uncore, dram)
  - `path`: Hardware sensor path
- **Constant Labels**:
  - `node_name`: Name of the node

#### kepler_node_cpu_active_watts

- **Type**: GAUGE
- **Description**: Power consumption of CPU in active state at node level in watts
- **Labels**:
  - `zone`: Energy zone (package, core, uncore, dram)
  - `path`: Hardware sensor path
- **Constant Labels**:
  - `node_name`: Name of the node

#### kepler_node_cpu_idle_joules_total

- **Type**: COUNTER
- **Description**: Energy consumption of CPU in idle state at node level in joules
- **Labels**:
  - `zone`: Energy zone (package, core, uncore, dram)
  - `path`: Hardware sensor path
- **Constant Labels**:
  - `node_name`: Name of the node

#### kepler_node_cpu_idle_watts

- **Type**: GAUGE
- **Description**: Power consumption of CPU in idle state at node level in watts
- **Labels**:
  - `zone`: Energy zone (package, core, uncore, dram)
  - `path`: Hardware sensor path
- **Constant Labels**:
  - `node_name`: Name of the node

#### kepler_node_cpu_usage_ratio

- **Type**: GAUGE
- **Description**: CPU usage ratio of a node (value between 0.0 and 1.0)
- **Constant Labels**:
  - `node_name`: Name of the node

#### kepler_node_cpu_info

- **Type**: GAUGE
- **Description**: CPU information from procfs
- **Labels**:
  - `processor`: Processor number
  - `vendor_id`: CPU vendor ID
  - `model_name`: CPU model name
  - `physical_id`: Physical CPU ID
  - `core_id`: Core ID

### Container Metrics

These metrics provide energy and power information for individual containers.

#### kepler_container_cpu_joules_total

- **Type**: COUNTER
- **Description**: Total energy consumption of CPU at container level in joules
- **Labels**:
  - `container_id`: Container identifier
  - `container_name`: Container name
  - `runtime`: Container runtime (docker, containerd, cri-o, podman)
  - `state`: Container state (running, terminated)
  - `zone`: Energy zone (package, core, uncore, dram)
  - `pod_id`: Pod identifier (if running in Kubernetes)
- **Constant Labels**:
  - `node_name`: Name of the node

#### kepler_container_cpu_watts

- **Type**: GAUGE
- **Description**: Current power consumption of CPU at container level in watts
- **Labels**:
  - `container_id`: Container identifier
  - `container_name`: Container name
  - `runtime`: Container runtime (docker, containerd, cri-o, podman)
  - `state`: Container state (running, terminated)
  - `zone`: Energy zone (package, core, uncore, dram)
  - `pod_id`: Pod identifier (if running in Kubernetes)
- **Constant Labels**:
  - `node_name`: Name of the node

### Process Metrics

These metrics provide energy and power information for individual processes.

#### kepler_process_cpu_joules_total

- **Type**: COUNTER
- **Description**: Total energy consumption of CPU at process level in joules
- **Labels**:
  - `pid`: Process ID
  - `comm`: Process command name
  - `exe`: Process executable path
  - `type`: Process type (container, vm, regular)
  - `state`: Process state (running, terminated)
  - `container_id`: Container ID (if process runs in container)
  - `vm_id`: VM ID (if process runs in VM)
  - `zone`: Energy zone (package, core, uncore, dram)
- **Constant Labels**:
  - `node_name`: Name of the node

#### kepler_process_cpu_watts

- **Type**: GAUGE
- **Description**: Current power consumption of CPU at process level in watts
- **Labels**:
  - `pid`: Process ID
  - `comm`: Process command name
  - `exe`: Process executable path
  - `type`: Process type (container, vm, regular)
  - `state`: Process state (running, terminated)
  - `container_id`: Container ID (if process runs in container)
  - `vm_id`: VM ID (if process runs in VM)
  - `zone`: Energy zone (package, core, uncore, dram)
- **Constant Labels**:
  - `node_name`: Name of the node

#### kepler_process_cpu_seconds_total

- **Type**: COUNTER
- **Description**: Total user and system CPU time at process level in seconds
- **Labels**:
  - `pid`: Process ID
  - `comm`: Process command name
  - `exe`: Process executable path
  - `type`: Process type (container, vm, regular)
  - `container_id`: Container ID (if process runs in container)
  - `vm_id`: VM ID (if process runs in VM)
- **Constant Labels**:
  - `node_name`: Name of the node

### Virtual Machine Metrics

These metrics provide energy and power information for virtual machines.

#### kepler_vm_cpu_joules_total

- **Type**: COUNTER
- **Description**: Total energy consumption of CPU at VM level in joules
- **Labels**:
  - `vm_id`: Virtual machine identifier
  - `vm_name`: Virtual machine name
  - `hypervisor`: Hypervisor type (kvm, qemu)
  - `state`: VM state (running, terminated)
  - `zone`: Energy zone (package, core, uncore, dram)
- **Constant Labels**:
  - `node_name`: Name of the node

#### kepler_vm_cpu_watts

- **Type**: GAUGE
- **Description**: Current power consumption of CPU at VM level in watts
- **Labels**:
  - `vm_id`: Virtual machine identifier
  - `vm_name`: Virtual machine name
  - `hypervisor`: Hypervisor type (kvm, qemu)
  - `state`: VM state (running, terminated)
  - `zone`: Energy zone (package, core, uncore, dram)
- **Constant Labels**:
  - `node_name`: Name of the node

### Pod Metrics

These metrics provide energy and power information for Kubernetes pods.

#### kepler_pod_cpu_joules_total

- **Type**: COUNTER
- **Description**: Total energy consumption of CPU at pod level in joules
- **Labels**:
  - `pod_id`: Pod identifier
  - `pod_name`: Pod name
  - `pod_namespace`: Pod namespace
  - `state`: Pod state (running, terminated)
  - `zone`: Energy zone (package, core, uncore, dram)
- **Constant Labels**:
  - `node_name`: Name of the node

#### kepler_pod_cpu_watts

- **Type**: GAUGE
- **Description**: Current power consumption of CPU at pod level in watts
- **Labels**:
  - `pod_id`: Pod identifier
  - `pod_name`: Pod name
  - `pod_namespace`: Pod namespace
  - `state`: Pod state (running, terminated)
  - `zone`: Energy zone (package, core, uncore, dram)
- **Constant Labels**:
  - `node_name`: Name of the node

### Build Information Metrics

#### kepler_build_info

- **Type**: GAUGE
- **Description**: A metric with a constant '1' value labeled with version information
- **Labels**:
  - `arch`: CPU architecture
  - `branch`: Git branch
  - `revision`: Git revision
  - `version`: Kepler version
  - `goversion`: Go version used to build

## Power Attribution Algorithm

Kepler distributes energy consumption from hardware sensors to workloads using the following algorithm:

1. **Read Hardware Sensors**: Collect total energy from RAPL (Running Average Power Limit) zones
2. **Calculate Node Usage**: Determine total CPU time and usage ratio from `/proc/stat`
3. **Split Node Energy**: Divide total energy into Active and Idle based on CPU usage ratio
4. **Process Attribution**: Calculate CPU time deltas for each workload
5. **Distribute Active Energy**: Allocate Active energy proportionally based on CPU utilization ratios
6. **Aggregate Workloads**: Sum process energy to container/VM/pod levels
7. **Handle Edge Cases**: Manage idle power, new/terminated processes, and counter wraparound

## Zone-Based Energy Sources

### RAPL (Running Average Power Limit)

RAPL is Intel's power capping mechanism that provides energy readings at different levels:

- **Package**: Complete CPU socket energy (cores + uncore)
- **Core (PP0)**: CPU cores energy (processor model dependent)
- **Uncore (PP1)**: Uncore components (last-level cache, integrated GPU, memory controller)
- **DRAM**: Memory energy consumption

### Zone Availability by Architecture

| Microarchitecture | Package | CORE (PP0) | UNCORE (PP1) | DRAM |
|---|---|---|---|---|
| Haswell | ✓ | ✓/✗ | ✓/✗ | ✓ |
| Broadwell | ✓ | ✓/✗ | ✓/✗ | ✓ |
| Skylake | ✓ | ✓ | ✓/✗ | ✓ |
| Kaby Lake | ✓ | ✓ | ✓/✗ | ✓ |

✓ = Available, ✗ = Not available (varies by consumer/server grade)

## Prometheus Queries

### Getting Power Consumption (Watts)

To get current power consumption in watts, use the gauge metrics directly:

```promql
# Container power consumption
kepler_container_cpu_watts{container_name="nginx"}

# Node power consumption by zone
kepler_node_cpu_watts{zone="package"}
```

### Getting Energy Consumption Rate (Watts from Counters)

To calculate power consumption from energy counters using rate functions:

```promql
# Container power consumption rate
rate(kepler_container_cpu_joules_total[1m])

# Node power consumption rate by zone
rate(kepler_node_cpu_joules_total{zone="package"}[1m])
```

### Aggregating Pod Energy

```promql
# Total pod energy consumption
sum by (pod_name, pod_namespace) (rate(kepler_pod_cpu_joules_total[1m]))
```

### Node Energy Breakdown

```promql
# Energy consumption by zone
sum by (zone) (rate(kepler_node_cpu_joules_total[1m]))
```

## Configuration

Energy metrics can be controlled through Kepler configuration:

### Metrics Levels

Configure which metric levels to export:

```yaml
exporter:
  prometheus:
    metricsLevel:
      - node      # Node-level metrics
      - process   # Process-level metrics
      - container # Container-level metrics
      - vm        # VM-level metrics
      - pod       # Pod-level metrics (requires Kubernetes)
```

### RAPL Zones

Filter which RAPL zones to monitor:

```yaml
rapl:
  zones: ["package", "core", "dram"]  # Empty array enables all available zones
```

For more configuration options, see the [Configuration Guide](../../usage/configuration.md).

## RAPL Power Domain

[RAPL power domains supported](https://zhenkai-zhang.github.io/papers/rapl.pdf) in some
recent Intel microarchitecture (consumer-grade/server-grade):

| Microarchitecture | Package | CORE (PP0) | UNCORE (PP1) | DRAM |
|---|---|---|---|---|
|      Haswell      |   Y/Y   |   Y/**N**  |    Y/**N**   |  Y/Y |
|     Broadwell     |   Y/Y   |   Y/**N**  |    Y/**N**   |  Y/Y |
|      Skylake      |   Y/Y   |     Y/Y    |    Y/**N**   |  Y/Y |
|     Kaby Lake     |   Y/Y   |     Y/Y    |    Y/**N**   |  Y/Y |

**Legend**: Y = Available, **N** = Not available (varies by consumer/server grade)
