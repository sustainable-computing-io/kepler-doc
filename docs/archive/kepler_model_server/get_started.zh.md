# Kepler 模型服务器入门指南

模型服务器项目为基于 Kepler 导出的能源相关指标的功率模型训练、导出、服务和利用
提供了工具。请按照以下步骤开始使用该项目。

## 第 1 步：了解管道

第一步是了解[训练管道](./pipeline.md)中的功率模型构建概念。

## 第 2 步：学习如何使用功率模型

### 选择估算器

---

根据模型格式，有两种使用模型的方式。如果模型格式可以直接在 Kepler 导出器内处理，
例如 `json` 格式的线性回归权重，则不需要额外配置。

但是，如果模型采用存档在 `zip` 中的通用格式，则需要通过环境变量或 Kepler
配置映射启用估算器 sidecar。

```bash
export NODE_COMPONENTS_ESTIMATOR=true
```

或

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
name: kepler-cfm
namespace: kepler
data:
    MODEL_CONFIG: |
        NODE_COMPONENTS_ESTIMATOR=true
```

### 选择功率模型

---

有两种获取功率模型的方式：静态和动态。

#### 静态配置

静态方式是直接从 `INIT_URL` 下载模型。可以通过环境变量直接设置或通过
`kepler-cfm` Kepler 配置映射设置。例如，

```bash
export NODE_COMPONENTS_INIT_URL= < 静态 URL >
```

或

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
name: kepler-cfm
namespace: kepler
data:
    MODEL_CONFIG: |
        NODE_COMPONENTS_INIT_URL= < 静态 URL >
```

提供的管道 v0.7 的静态 URL 在[这里](https://github.com/sustainable-computing-io/kepler-model-db/tree/main/models/v0.7)列出。

#### 通过服务器 API 动态获取

动态方式是启用模型服务器自动选择具有最佳准确性并支持运行集群环境的功率模型。
同样，可以通过环境变量设置或通过 Kepler 配置映射设置。

```bash
export MODEL_SERVER_ENABLE=true
```

或

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
name: kepler-cfm
namespace: kepler
data:
    MODEL_CONFIG: |
        MODEL_SERVER_ENABLE: "true"
```

在 [Kepler 功率估算部署](./power_estimation.md) 中查看更多内容

## 第 3 步：学习如何训练功率模型并回馈社区

如您所知，根据特定机器类型定制功率模型而不是依赖单一通用模型是至关重要的。
我们热切欢迎社区的贡献，通过模型服务器项目帮助在您的机器上构建替代功率模型。

有关模型训练的详细指导，请参阅我们的模型训练指南[这里](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/model_training)。
