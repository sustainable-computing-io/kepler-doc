# 训练流程

Kepler模型服务器可为不同场景和学习方法提供多种功耗模型。训练流程是对功耗模型训练的抽象，它将一组学习方法应用于不同的能源组合、功耗隔离方法及可用能耗相关指标。

## 流程概述

`pipeline`由三个步骤组成：`extract`（提取）、`isolate`（隔离）和`train`（训练），如下图所示。Kepler将能耗相关指标导出为Prometheus计数器（counter），该类型提供随时间累积的数值。

![流程示意图](../fig/pipeline_plot.png)

`extract`步骤将计数器指标转换为测量指标（gauge），类似于Prometheus的`rate()`函数，给出每秒的数值。该步骤还会为每个`feature group`（特征组）分别进行数据清洗。

从Prometheus查询获取的功耗值是实测功耗，由随工作负载变化的动态功耗（dynamic power）和空闲状态仍消耗的基础功耗（idle power）组成。

`isolate`步骤计算基础功耗，并隔离每个`energy source`（能源）的动态功耗。

`train`步骤应用每个`trainer`（训练器）基于预处理数据创建多个备选功耗模型。

> 我们计划未来针对每个节点/机器类型单独构建功耗模型。详见[节点类型](#node-type)章节。

- 关于`energy source`的详细信息请参阅[能源类型](#energy-source)章节
- 关于`feature group`的详细信息请参阅[特征组](#feature-group)章节  
- 关于`isolate`步骤及`AbsPower`、`DynPower`功耗模型概念请参阅[功耗隔离](#power-isolation)章节
- 可用`trainer`列表请查看[训练器](#trainer)章节

## 能源类型

`energy source`或`source`指提供能耗数值的来源（功率计）。每个能源提供一个或多个`energy components`（能源组件）。当前支持的能源如下：

能源/功率源 | 能源/功率组件
---|---
[rapl](../design/kepler-energy-sources.md) | package（封装）、core（核心）、uncore（非核心）、dram（内存）
[acpi](../design/kepler-energy-sources.md#using-kernel-driver-xgene-hwmon) | platform（平台）

## 特征组

`feature group`是基于基础设施上下文对可用特征的抽象，因为某些环境可能无法暴露部分指标。例如在私有云环境的虚拟机中，通常无法获取硬件计数器指标。因此模型会针对下表中定义的各资源利用率指标组进行训练。

组名 | 特征 | Kepler指标来源
---|---|---
CounterOnly | COUNTER_FEATURES | [硬件计数器](../design/metrics.md)
BPFOnly | BPF_FEATURES | [BPF](../design/metrics.md)
IRQOnly | IRQ_FEATURES | [IRQ](../design/metrics.md)
AcceleratorOnly | ACCELERATOR_FEATURES | [加速器](../design/metrics.md)
CounterIRQCombined | COUNTER_FEATURES, IRQ_FEATURES | BPF和硬件计数器
Basic | COUNTER_FEATURES, BPF_FEATURES | 除IRQ和节点信息外的所有指标
WorkloadOnly | COUNTER_FEATURES, BPF_FEATURES, IRQ_FEATURES, ACCELERATOR_FEATURES | 除节点信息外的所有指标
Full | WORKLOAD_FEATURES, SYSTEM_FEATURES | 全部指标

节点信息指[kepler_node_info](../design/metrics.md)指标的值。

## 功耗隔离

从Prometheus查询获取的功耗值是绝对功耗（AbsPower），即基础功耗与动态功耗之和（基础功耗表示系统静止状态下的功耗，动态功耗是随资源利用率增加的功耗，绝对功耗=基础功耗+动态功耗）。此外，该功耗还包含用户工作负载、后台进程和操作系统进程的总功耗。

`isolate`步骤应用机制从绝对功耗中分离出基础功耗，得到动态功耗。该步骤还实现了将后台和操作系统进程（称为`system_processes`）消耗的动态功耗分离的功能。

需注意，即使用户工作负载的资源利用率指标为零，基础功耗和`system_processes`动态功耗仍高于零。

目前有两种常用`isolator`（隔离器）：*ProfileIsolator*和*MinIdleIsolator*。

我们将使用隔离步骤训练的模型称为`DynPower`模型，而不使用隔离步骤训练的模型称为`AbsPower`模型。当前`DynPower`模型不包含基础功耗信息，但我们计划未来加入该信息。

*ProfileIsolator*依赖于在特定时间段内（不运行任何用户工作负载时）收集的数据（称为profile数据）。该隔离机制还会从训练数据中消除`system_processes`的资源利用率。

另一方面，*MinIdleIsolator*识别训练数据所有样本中的最小功耗值，假设该最小值同时代表基础功耗和`system_processes`功耗。

虽然我们也应从训练数据中移除最小资源利用率，但当前该隔离机制仍包含`system_processes`的资源利用率。不过我们计划未来移除该部分。

如果存在与给定`node_type`匹配的`profile data`，流程将使用*ProfileIsolator*预处理训练数据。否则将应用其他隔离机制（如*MinIdleIsolator*）。

（查看如何生成profile数据[请点击此处](./node_profile.md)）

### 讨论

关于使用`DynPower`还是`AbsPower`模型的选择仍在研究中。某些情况下DynPower比`AbsPower`表现出更好的准确性。但由于`DynPower`模型缺乏基础功耗信息，我们当前使用`AbsPower`模型来估算节点在Platform、CPU和DRAM组件上的功耗。

需要说明的是，在公有云环境的VM中暴露基础功耗是不可能的。因为宿主机的基础功耗必须分配给宿主机上所有运行的VM，而在公有云环境中无法确定宿主机上运行的VM数量。

因此，只有在节点上仅运行单个VM的特定场景下，或在裸机环境中使用功耗模型时，我们才能暴露基础功耗。

## 训练器

`trainer`是定义学习方法的抽象，该方法应用于每个特征组及给定的功耗标注源。

可用训练器（v0.6版本）：
- 多项式回归训练器
- 梯度提升回归训练器
- 随机梯度下降回归训练器
- K近邻回归训练器
- 线性回归训练器
- 支持向量回归训练器

## 节点类型

Kepler根据机器（节点）的基准测试性能将其分为若干组，并为每个组单独训练模型。已识别的分组以`node type`（节点类型）形式导出。