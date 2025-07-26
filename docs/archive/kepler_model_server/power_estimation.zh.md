# Kepler 功耗估算部署方案

在Kepler中，我们还为未安装或未支持功耗测量工具的系统提供基于资源使用情况的功耗估算解决方案。目前提供两种估算器选择。

## 估算器类型

- **本地线性回归估算器**：该估算器使用训练好的权重乘以标准化后的使用指标值（线性回归模型）进行功耗估算。

- **通用估算器Sidecar**：此估算器会对使用指标进行转换，并应用训练好的模型，这些模型可以是scikit-learn库中的任何回归模型或Keras（TensorFlow）中的神经网络。要使用此估算器，需要启用Kepler估算器功能。

此外，训练好的模型和权重可以通过连接Kepler模型服务器API，通过在线训练流程定期更新。

## 部署场景

### 最小化部署

最小化部署方案是在Kepler主容器中使用本地线性回归估算器，仅使用离线训练的模型权重。

![最小化部署](../fig/minimum_deploy.png)

### 带通用估算器Sidecar的部署

要启用通用估算器进行功耗推断，可以按下图所示部署估算器sidecar。两个容器之间通过Unix域套接字连接，这种方式轻量且快速。与本地估算器不同，通用估算器sidecar配备了多个支持推断的库和依赖项。这种额外开销需要与模型灵活性带来的估算精度提升进行权衡。

![估算器集成](../fig/disable_model_server.png)

### 连接Kepler模型服务器的最小化部署

为了获取预期能提供更好估算精度的更新权重，Kepler可以连接到远程Kepler模型服务器，该服务器使用来自配备功耗测量工具系统的数据进行在线训练，如下图所示。

![模型服务器集成](../fig/disable_estimator_sidecar.png)

### 完整部署

下图展示了启用Kepler通用估算器并同时连接远程Kepler模型服务器的部署方案。Kepler通用估算器sidecar可以动态更新来自Kepler模型服务器的模型，预期能获得最准确的模型。

![完整集成](../fig/full_integration.png)

## Kepler模型数据库提供的功耗模型

版本 | 功耗数据源 | 流水线 | 可用能源源 | 错误报告
---|---|---|---|---
[0.6](https://github.com/sustainable-computing-io/kepler-model-db/tree/main/models/v0.6) | [nx12](https://github.com/sustainable-computing-io/kepler-model-db/tree/main/models/v0.6/nx12) | [std_v0.6](https://github.com/sustainable-computing-io/kepler-model-db/blob/main/models/v0.6/.doc/std_v0.6.md) | rapl,acpi | [链接](https://github.com/sustainable-computing-io/kepler-model-db/blob/main/models/v0.6/nx12/README.md)
[0.7](https://github.com/sustainable-computing-io/kepler-model-db/tree/main/models/v0.7) | [SPECpower](https://www.spec.org/power_ssj2008/) | [specpower](https://github.com/sustainable-computing-io/kepler-model-db/blob/main/models/v0.7/.doc/specpower.md) | acpi | [链接](https://github.com/sustainable-computing-io/kepler-model-db/tree/main/models/v0.7/specpower)
[0.7](https://github.com/sustainable-computing-io/kepler-model-db/tree/main/models/v0.7) | [训练手册](https://github.com/sustainable-computing-io/kepler-model-training-playbook) | [ec2](https://github.com/sustainable-computing-io/kepler-model-db/blob/main/models/v0.7/.doc/ec2.md) | intel_rapl | [链接](https://github.com/sustainable-computing-io/kepler-model-db/tree/main/models/v0.7/ec2)