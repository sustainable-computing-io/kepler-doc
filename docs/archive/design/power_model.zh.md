# Kepler 功耗模型

在Kepler中，根据可用测量指标，我们通过混合两种功耗建模方法提供容器级功耗数据：

## 建模方法

- **功耗比例建模**：该模型通过计算使用量与总功耗的占比来生成更细粒度的功耗数据。当总功耗可测量时，此方法为默认建模方式。

- **功耗估算建模**：该模型将使用量指标作为训练模型的特征输入来估算功耗。即使无法直接测量功耗指标时仍可使用此方法。估算可在三个层级进行：节点总功耗（包含风扇、电源等）、节点内部组件功耗（如CPU、内存）、容器组功耗。

    !!! 注意  
        另请参阅[Kepler模型服务器入门指南](../kepler_model_server/get_started.md)

- **预训练功耗模型**：我们为不同部署场景提供预训练模型。当前x86_64架构的预训练模型基于[Intel® Xeon® Processor E5-2667 v3][1]开发，其他架构模型即将推出。这些模型存放于[Kepler模型数据库][2]，支持RAPL和ACPI两种电源的功耗比例建模与估算建模。其中`AbsPower`模型可估算空闲与动态功耗，而`DynPower`模型仅估算动态功耗。模型MAE（平均绝对误差）值已同步发布。Kepler容器镜像已预加载[acpi/AbsPower/BPFOnly/SGDRegressorTrainer_1.json][3]模型用于节点能耗估算，以及[rapl/AbsPower/BPFOnly/SGDRegressorTrainer_1.json][4]模型用于容器绝对功耗估算。

## 使用场景

场景 | 节点总功耗 | 节点组件功耗 | 容器组功耗
---|---|---|---
物理机（x86带功耗计）| 直接测量（如ACPI）| 直接测量（RAPL）| 功耗比例
物理机（x86无功耗计）| 功耗估算 | 直接测量 | 功耗比例
物理机（非x86带功耗计） | 直接测量 | 功耗估算 | 功耗比例 
物理机（非x86无功耗计） | 功耗估算 | 功耗估算 | 功耗比例
虚拟机（透传物理机x86带功耗计）|测量值+虚拟机映射|测量值+虚拟机映射|功耗比例
虚拟机（透传物理机x86无功耗计）|功耗估算|测量值+虚拟机映射|功耗比例
虚拟机（透传物理机非x86带功耗计）|测量值+虚拟机映射|功耗估算|功耗比例
虚拟机（带节点信息）|功耗估算|功耗估算|功耗比例
纯虚拟机|-|-|功耗估算

[1]:https://github.com/sustainable-computing-io/kepler-model-db/tree/main/models
[2]:https://github.com/sustainable-computing-io/kepler-model-db/tree/main/models/v0.6/nx12
[3]:https://github.com/sustainable-computing-io/kepler-model-db/blob/main/models/v0.6/nx12/std_v0.6/acpi/AbsPower/BPFOnly/SGDRegressorTrainer_1.json
[4]:https://github.com/sustainable-computing-io/kepler-model-db/blob/main/models/v0.6/nx12/std_v0.6/rapl/AbsPower/BPFOnly/SGDRegressorTrainer_1.json

（注：保留所有技术术语英文原名如RAPL/ACPI/MAE等，BM根据上下文译为"物理机"，VM译为"虚拟机"，Power Ratio保持为"功耗比例"以准确传达技术概念）