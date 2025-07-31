# Kepler功率模型/运行方式

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

在Kepler中，根据可用的测量结果，我们通过两种功率建模方法的混合提供了提供Pod级别功率：

## 建模方法
-**功率比建模**：该建模通过功率总和的使用率来计算更细粒度的功率。当总功率已知时，默认情况下会使用此建模。

-**功率估计建模**：该建模通过使用度量作为训练模型的输入特征来估计功率。即使不能测量功率度量，也可以使用此建模。估计可以分为三个级别：节点总功率（包括风扇、电源等）、节点内部组件功率（如CPU、内存）、Pod功率。另请参阅[开始使用Kepler模型服务器](../kepler_model_server/get_started.md)

-**预训练功率模型**：我们为不同的部署场景提供预训练的功率模型。当前的x86_64预训练模型是在[Intel® Xeon® Processor E5-2667 v3](https://github.com/sustainable-computing-io/kepler-model-db/tree/main/models)中开发的。其他架构的模型即将推出。您可以在[Kepler Model DB](https://github.com/sustainable-computing-io/kepler-model-db/tree/main/models/v0.6/nx12)中找到这些模型。这些模型支持RAPL和ACPI电源的功率比例建模和功率估算建模。AbsPower模型估算静态和动态功率，而DynPower模型只估算动态功率。这些模型的MAE（平均绝对误差）也已发布。Kepler容器镜像已预加载[acpi/AbsPower/BPFOnly/SGDRegressorTrainer_1.json](https://github.com/sustainable-computing-io/kepler-model-db/blob/main/models/v0.6/nx12/std_v0.6/acpi/AbsPower/BPFOnly/SGDRegressorTrainer_1.json)模型用于节点能量估算，以及[rapl/AbsPower/BPFOnly/SGDRegressorTrainer_1.json](https://github.com/sustainable-computing-io/kepler-model-db/blob/main/models/v0.6/nx12/std_v0.6/rapl/AbsPower/BPFOnly/SGDRegressorTrainer_1.json)用于容器绝对功率估算。

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
