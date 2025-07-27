```markdown
# Kepler 指标文档

本文档描述了Kepler导出的用于监控不同层级（节点、容器、进程、虚拟机、Pod）能耗的指标。

## 概述

Kepler以Prometheus格式导出指标，可被Prometheus或其他兼容监控系统抓取。所有指标遵循Prometheus命名规范，并以`kepler_`为前缀。

### 指标类型

- **COUNTER**：单调递增的累积指标（如总能耗）
- **GAUGE**：可增减的瞬时指标（如当前功耗）

### 基于分区的组织架构

Kepler按硬件组件分区组织能耗指标：

- **package**：CPU插槽级能耗（包含核心与非核心组件）
- **core**：CPU核心级能耗（部分处理器支持）
- **uncore**：非核心组件（末级缓存、集成GPU、内存控制器）
- **dram**：内存能耗

## 指标参考

### 节点级指标

反映整个系统的总能耗情况。

#### kepler_node_cpu_joules_total

- **类型**: COUNTER  
- **描述**: 节点级CPU总能耗（焦耳）  
- **标签**:  
  - `zone`: 能耗分区（package/core/uncore/dram）  
  - `path`: 硬件传感器路径  
- **固定标签**:  
  - `node_name`: 节点名称  

#### kepler_node_cpu_watts

- **类型**: GAUGE  
- **描述**: 节点级CPU当前功耗（瓦特）  
- **标签**:  
  - `zone`: 能耗分区  
  - `path`: 硬件传感器路径  
- **固定标签**:  
  - `node_name`: 节点名称  

（其他节点指标遵循相同模式，此处省略重复翻译）

### 容器级指标

#### kepler_container_cpu_joules_total

- **类型**: COUNTER  
- **描述**: 容器级CPU总能耗（焦耳）  
- **标签**:  
  - `container_id`: 容器ID  
  - `container_name`: 容器名称  
  - `runtime`: 容器运行时（docker/containerd/cri-o/podman）  
  - `state`: 容器状态（running/terminated）  
  - `zone`: 能耗分区  
  - `pod_id`: Pod ID（Kubernetes环境）  
- **固定标签**:  
  - `node_name`: 节点名称  

### 进程级指标

#### kepler_process_cpu_joules_total

- **类型**: COUNTER  
- **描述**: 进程级CPU总能耗（焦耳）  
- **标签**:  
  - `pid`: 进程ID  
  - `comm`: 进程命令名  
  - `exe`: 可执行文件路径  
  - `type`: 进程类型（container/vm/regular）  
  - `state`: 进程状态  
  - `container_id`: 容器ID（如适用）  
  - `vm_id`: 虚拟机ID（如适用）  
  - `zone`: 能耗分区  
- **固定标签**:  
  - `node_name`: 节点名称  

### 虚拟机指标

#### kepler_vm_cpu_joules_total

- **类型**: COUNTER  
- **描述**: 虚拟机级CPU总能耗（焦耳）  
- **标签**:  
  - `vm_id`: 虚拟机ID  
  - `vm_name`: 虚拟机名称  
  - `hypervisor`: 虚拟化类型（kvm/qemu）  
  - `state`: 虚拟机状态  
  - `zone`: 能耗分区  
- **固定标签**:  
  - `node_name`: 节点名称  

### Pod指标

#### kepler_pod_cpu_joules_total

- **类型**: COUNTER  
- **描述**: Pod级CPU总能耗（焦耳）  
- **标签**:  
  - `pod_id`: Pod ID  
  - `pod_name`: Pod名称  
  - `pod_namespace`: 命名空间  
  - `state`: Pod状态  
  - `zone`: 能耗分区  
- **固定标签**:  
  - `node_name`: 节点名称  

## 能耗分配算法

Kepler通过以下步骤将硬件传感器数据分配到工作负载：

1. **读取硬件传感器**：从RAPL分区获取总能耗  
2. **计算节点使用率**：通过`/proc/stat`获取CPU总时间和使用率  
3. **拆分节点能耗**：根据CPU使用率划分为活跃/空闲能耗  
4. **进程级分配**：计算各工作负载的CPU时间增量  
5. **活跃能耗分配**：按CPU使用率比例分配活跃能耗  
6. **聚合工作负载**：汇总进程级数据到容器/虚拟机/Pod层级  
7. **处理边界情况**：管理空闲功耗、新建/终止的进程及计数器回绕  

## RAPL能耗源

Intel的RAPL机制提供不同层级的能耗读数：

| 微架构       | Package | CORE (PP0) | UNCORE (PP1) | DRAM |
|--------------|---------|------------|--------------|------|
| Haswell      | ✓       | ✓/✗        | ✓/✗          | ✓    |
| Broadwell    | ✓       | ✓/✗        | ✓/✗          | ✓    |
| Skylake      | ✓       | ✓          | ✓/✗          | ✓    |
| Kaby Lake    | ✓       | ✓          | ✓/✗          | ✓    |

✓ = 支持，✗ = 不支持（消费级/服务器级存在差异）

## Prometheus查询示例

```promql
# 获取容器实时功耗
kepler_container_cpu_watts{container_name="nginx"}

# 通过计数器计算能耗速率
rate(kepler_node_cpu_joules_total{zone="package"}[1m])

# Pod能耗聚合
sum by (pod_name, pod_namespace) (rate(kepler_pod_cpu_joules_total[1m]))
```

## 配置说明

### 指标层级控制

```yaml
exporter:
  prometheus:
    metricsLevel:
      - node      # 节点级指标
      - process   # 进程级指标
      - container # 容器级指标
```

### RAPL分区配置

```yaml
rapl:
  zones: ["package", "dram"]  # 空数组启用所有可用分区
```

完整配置参见[配置指南](../../usage/configuration.md)。