# Kepler功率模型/运行方式

在Kepler中，根据可用的测量结果，我们通过两种功率建模方法的混合提供了提供Pod级别功率：

## 建模方法
-**功率比建模**：该建模通过功率总和的使用率来计算更细粒度的功率。当总功率已知时，默认情况下会使用此建模。

-**功率估计建模**：该建模通过使用度量作为训练模型的输入特征来估计功率。即使不能测量功率度量，也可以使用此建模。估计可以分为三个级别：节点总功率（包括风扇、电源等）、节点内部组件功率（如CPU、内存）、Pod功率。另请参阅[开始使用Kepler模型服务器](../kepler_model_server/get_started.md)

## 使用场景

Scenario | Node Total Power | Node Component Powers | Pod Power
---|---|---|---
BM (x86 with power meter)| Measurement (e.g., ACPI)|  Measurement (RAPL)| Power Ratio
BM (x86 but no power meter)| Power Estimation | Measurement| Power Ratio
BM (non-x86 with power meter) | Measurement | Power Estimation | Power Ratio
BM (non-x86 and no power meter) | Power Estimation | Power Estimation | Power Ratio
VM with node info and power passthrough from BM (x86 with power meter)|Measurement + VM Mapping|Measurement + VM Mapping|Power Ratio
VM with node info and power passthrough from BM (x86 but no power meter)|Power Estimation|Measurement + VM Mapping|Power Ratio
VM with node info and power passthrough from BM (non-x86 with power meter)|Measurement + VM Mapping|Power Estimation|Power Ratio
VM with node info|Power Estimation|Power Estimation|Power Ratio
Pure VM|\-|\-|Power Estimation
|||