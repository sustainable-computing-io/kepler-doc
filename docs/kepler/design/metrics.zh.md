# Kepler 指标

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

本文档描述了 Kepler 导出的指标，用于监控各个级别（节点、容器、进程、虚拟机）的能耗。

## 概述

Kepler 以 Prometheus 格式导出指标，可以被 Prometheus 或其他兼容的监控系统抓取。

### 指标类型

- **COUNTER**：随时间只增加的累积指标
- **GAUGE**：可以增加和减少的指标

## 指标参考

### 节点指标

这些指标在节点级别提供能量和功率信息。

#### kepler_node_cpu_active_joules_total

- **类型**：COUNTER
- **描述**：节点级别 CPU 在活动状态的能耗，单位为焦耳
- **标签**：
  - `zone`
  - `path`
- **常量标签**：
  - `node_name`

#### kepler_node_cpu_active_watts

- **类型**：GAUGE
- **描述**：节点级别 CPU 在活动状态的功耗，单位为瓦特
- **标签**：
  - `zone`
  - `path`
- **常量标签**：
  - `node_name`

#### kepler_node_cpu_idle_joules_total

- **类型**：COUNTER
- **描述**：节点级别 CPU 在空闲状态的能耗，单位为焦耳
- **标签**：
  - `zone`
  - `path`
- **常量标签**：
  - `node_name`

#### kepler_node_cpu_idle_watts

- **类型**：GAUGE
- **描述**：节点级别 CPU 在空闲状态的功耗，单位为瓦特
- **标签**：
  - `zone`
  - `path`
- **常量标签**：
  - `node_name`

#### kepler_node_cpu_info

- **类型**：GAUGE
- **描述**：来自 procfs 的 CPU 信息
- **标签**：
  - `processor`
  - `vendor_id`
  - `model_name`
  - `physical_id`
  - `core_id`

#### kepler_node_cpu_joules_total

- **类型**：COUNTER
- **描述**：节点级别 CPU 的能耗，单位为焦耳
- **标签**：
  - `zone`
  - `path`
- **常量标签**：
  - `node_name`

#### kepler_node_cpu_usage_ratio

- **类型**：GAUGE
- **描述**：节点的 CPU 使用率（值在 0.0 和 1.0 之间）
- **常量标签**：
  - `node_name`

#### kepler_node_cpu_watts

- **类型**：GAUGE
- **描述**：节点级别 CPU 的功耗，单位为瓦特
- **标签**：
  - `zone`
  - `path`
- **常量标签**：
  - `node_name`

### 容器指标

这些指标为容器提供能量和功率信息。

#### kepler_container_cpu_joules_total

- **类型**：COUNTER
- **描述**：容器级别 CPU 的能耗，单位为焦耳
- **标签**：
  - `container_id`
  - `container_name`
  - `runtime`
  - `state`
  - `zone`
  - `pod_id`
- **常量标签**：
  - `node_name`

#### kepler_container_cpu_watts

- **类型**：GAUGE
- **描述**：容器级别 CPU 的功耗，单位为瓦特
- **标签**：
  - `container_id`
  - `container_name`
  - `runtime`
  - `state`
  - `zone`
  - `pod_id`
- **常量标签**：
  - `node_name`

### 进程指标

这些指标为单个进程提供能量和功率信息。

#### kepler_process_cpu_joules_total

- **类型**：COUNTER
- **描述**：进程级别 CPU 的能耗，单位为焦耳
- **标签**：
  - `pid`
  - `comm`
  - `exe`
  - `type`
  - `state`
  - `container_id`
  - `vm_id`
  - `zone`
- **常量标签**：
  - `node_name`

#### kepler_process_cpu_seconds_total

- **类型**：COUNTER
- **描述**：进程级别 CPU 的总用户和系统时间，单位为秒
- **标签**：
  - `pid`
  - `comm`
  - `exe`
  - `type`
  - `container_id`
  - `vm_id`
- **常量标签**：
  - `node_name`

#### kepler_process_cpu_watts

- **类型**：GAUGE
- **描述**：进程级别 CPU 的功耗，单位为瓦特
- **标签**：
  - `pid`
  - `comm`
  - `exe`
  - `type`
  - `state`
  - `container_id`
  - `vm_id`
  - `zone`
- **常量标签**：
  - `node_name`

### 虚拟机指标

这些指标为虚拟机提供能量和功率信息。

#### kepler_vm_cpu_joules_total

- **类型**：COUNTER
- **描述**：虚拟机级别 CPU 的能耗，单位为焦耳
- **标签**：
  - `vm_id`
  - `vm_name`
  - `hypervisor`
  - `state`
  - `zone`
- **常量标签**：
  - `node_name`

#### kepler_vm_cpu_watts

- **类型**：GAUGE
- **描述**：虚拟机级别 CPU 的功耗，单位为瓦特
- **标签**：
  - `vm_id`
  - `vm_name`
  - `hypervisor`
  - `state`
  - `zone`
- **常量标签**：
  - `node_name`

### Pod 指标

这些指标为 Pod 提供能量和功率信息。

#### kepler_pod_cpu_joules_total

- **类型**：COUNTER
- **描述**：Pod 级别 CPU 的能耗，单位为焦耳
- **标签**：
  - `pod_id`
  - `pod_name`
  - `pod_namespace`
  - `state`
  - `zone`
- **常量标签**：
  - `node_name`

#### kepler_pod_cpu_watts

- **类型**：GAUGE
- **描述**：Pod 级别 CPU 的功耗，单位为瓦特
- **标签**：
  - `pod_id`
  - `pod_name`
  - `pod_namespace`
  - `state`
  - `zone`
- **常量标签**：
  - `node_name`

### 其他指标

Kepler 提供的其他指标。

#### kepler_build_info

- **类型**：GAUGE
- **描述**：带有版本信息标签的常量值为 '1' 的指标
- **标签**：
  - `arch`
  - `branch`
  - `revision`
  - `version`
  - `goversion`

---

本文档由 gen-metric-docs 工具自动生成。
