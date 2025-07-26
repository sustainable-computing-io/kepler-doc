# Kepler 指标文档

本文档描述Kepler导出的用于监控各层级（节点、容器、进程、虚拟机）能耗的指标。

## 概述

Kepler以Prometheus格式导出指标，可被Prometheus或其他兼容的监控系统抓取。

### 指标类型

- **COUNTER**：累积型指标，仅随时间增长
- **GAUGE**：可增可减的指标

## 指标参考

### 节点指标

提供节点级别的能耗和功率信息。

#### kepler_node_cpu_active_joules_total

- **类型**: COUNTER  
- **描述**: 节点级别CPU活跃状态下的能耗（单位：焦耳）  
- **标签**:  
  - `zone`  
  - `path`  
- **固定标签**:  
  - `node_name`  

#### kepler_node_cpu_active_watts

- **类型**: GAUGE  
- **描述**: 节点级别CPU活跃状态下的功率（单位：瓦特）  
- **标签**:  
  - `zone`  
  - `path`  
- **固定标签**:  
  - `node_name`  

#### kepler_node_cpu_idle_joules_total

- **类型**: COUNTER  
- **描述**: 节点级别CPU空闲状态下的能耗（单位：焦耳）  
- **标签**:  
  - `zone`  
  - `path`  
- **固定标签**:  
  - `node_name`  

#### kepler_node_cpu_idle_watts

- **类型**: GAUGE  
- **描述**: 节点级别CPU空闲状态下的功率（单位：瓦特）  
- **标签**:  
  - `zone`  
  - `path`  
- **固定标签**:  
  - `node_name`  

#### kepler_node_cpu_info

- **类型**: GAUGE  
- **描述**: 来自procfs的CPU信息  
- **标签**:  
  - `processor`  
  - `vendor_id`  
  - `model_name`  
  - `physical_id`  
  - `core_id`  

#### kepler_node_cpu_joules_total

- **类型**: COUNTER  
- **描述**: 节点级别CPU总能耗（单位：焦耳）  
- **标签**:  
  - `zone`  
  - `path`  
- **固定标签**:  
  - `node_name`  

#### kepler_node_cpu_usage_ratio

- **类型**: GAUGE  
- **描述**: 节点CPU使用率（0.0到1.0之间的值）  
- **固定标签**:  
  - `node_name`  

#### kepler_node_cpu_watts

- **类型**: GAUGE  
- **描述**: 节点级别CPU总功率（单位：瓦特）  
- **标签**:  
  - `zone`  
  - `path`  
- **固定标签**:  
  - `node_name`  

### 容器指标

提供容器级别的能耗和功率信息。

#### kepler_container_cpu_joules_total

- **类型**: COUNTER  
- **描述**: 容器级别CPU能耗（单位：焦耳）  
- **标签**:  
  - `container_id`  
  - `container_name`  
  - `runtime`  
  - `state`  
  - `zone`  
  - `pod_id`  
- **固定标签**:  
  - `node_name`  

#### kepler_container_cpu_watts

- **类型**: GAUGE  
- **描述**: 容器级别CPU功率（单位：瓦特）  
- **标签**:  
  - `container_id`  
  - `container_name`  
  - `runtime`  
  - `state`  
  - `zone`  
  - `pod_id`  
- **固定标签**:  
  - `node_name`  

### 进程指标

提供进程级别的能耗和功率信息。

#### kepler_process_cpu_joules_total

- **类型**: COUNTER  
- **描述**: 进程级别CPU能耗（单位：焦耳）  
- **标签**:  
  - `pid`  
  - `comm`  
  - `exe`  
  - `type`  
  - `state`  
  - `container_id`  
  - `vm_id`  
  - `zone`  
- **固定标签**:  
  - `node_name`  

#### kepler_process_cpu_seconds_total

- **类型**: COUNTER  
- **描述**: 进程级别CPU总用户和系统时间（单位：秒）  
- **标签**:  
  - `pid`  
  - `comm`  
  - `exe`  
  - `type`  
  - `container_id`  
  - `vm_id`  
- **固定标签**:  
  - `node_name`  

#### kepler_process_cpu_watts

- **类型**: GAUGE  
- **描述**: 进程级别CPU功率（单位：瓦特）  
- **标签**:  
  - `pid`  
  - `comm`  
  - `exe`  
  - `type`  
  - `state`  
  - `container_id`  
  - `vm_id`  
  - `zone`  
- **固定标签**:  
  - `node_name`  

### 虚拟机指标

提供虚拟机级别的能耗和功率信息。

#### kepler_vm_cpu_joules_total

- **类型**: COUNTER  
- **描述**: 虚拟机级别CPU能耗（单位：焦耳）  
- **标签**:  
  - `vm_id`  
  - `vm_name`  
  - `hypervisor`  
  - `state`  
  - `zone`  
- **固定标签**:  
  - `node_name`  

#### kepler_vm_cpu_watts

- **类型**: GAUGE  
- **描述**: 虚拟机级别CPU功率（单位：瓦特）  
- **标签**:  
  - `vm_id`  
  - `vm_name`  
  - `hypervisor`  
  - `state`  
  - `zone`  
- **固定标签**:  
  - `node_name`  

### Pod指标

提供Pod级别的能耗和功率信息。

#### kepler_pod_cpu_joules_total

- **类型**: COUNTER  
- **描述**: Pod级别CPU能耗（单位：焦耳）  
- **标签**:  
  - `pod_id`  
  - `pod_name`  
  - `pod_namespace`  
  - `state`  
  - `zone`  
- **固定标签**:  
  - `node_name`  

#### kepler_pod_cpu_watts

- **类型**: GAUGE  
- **描述**: Pod级别CPU功率（单位：瓦特）  
- **标签**:  
  - `pod_id`  
  - `pod_name`  
  - `pod_namespace`  
  - `state`  
  - `zone`  
- **固定标签**:  
  - `node_name`  

### 其他指标

Kepler提供的附加指标。

#### kepler_build_info

- **类型**: GAUGE  
- **描述**: 带有版本信息的常量指标（值为1）  
- **标签**:  
  - `arch`  
  - `branch`  
  - `revision`  
  - `version`  
  - `goversion`  

---

本文档由gen-metric-docs工具自动生成。