# Kepler 模型服务器架构

Kepler 模型服务器是 Kepler 的补充项目，用于支持功耗模型的训练与部署服务。该项目构建了一个生态系统，能够从一个环境中收集指标，通过[管道框架](./pipeline.md)训练功耗模型，并将模型部署到另一个无法直接使用功率计（能耗测量设备）的环境中。

![模型服务器组件](../fig/model-server-components-simplified.png)

**管道输入：** 训练工作负载运行期间从 Prometheus 获取的查询结果。

**管道输出：** 包含归档的绝对功耗模型和动态功耗模型的目录，这些模型由每个可用特征组训练得出，并按能量源进行分类标记。

```sh
[管道名称]/[能量源]/[模型类型]/[特征组]/[归档模型]
```

- **管道名称** 用于区分不同建模方法的唯一标识，包括不同的提取器、隔离器、训练器组合、支持的特征组和能量源。
- [**能量/功率源**](./pipeline.md#energy-source) 作为功率标签来源的功率计。
- [**模型类型**](./pipeline.md#power-isolation) 区分是否包含后台隔离的模型类别。
- [**特征组**](./pipeline.md#feature-group) 作为模型输入来源的利用率指标组。
- **归档模型** 以`[训练器名称]_[节点类型]`格式命名的文件夹和压缩文件，其中训练器名称指代训练方案（如`GradientBoostingRegressor`），节点类型指用于训练的服务器[特征画像](./node_profile.md)分类。文件夹包含：
  - metadata.json
  - 模型文件
  - weight.json（本地估算器支持模型的权重文件，如线性回归模型（LR））
  - 特征工程（fe）文件

GitHub 项目地址 ➡️ [Kepler Model Server](https://github.com/sustainable-computing-io/kepler-model-server)