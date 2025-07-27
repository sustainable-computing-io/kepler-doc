# 开始使用Kepler模型服务器

模型服务器项目提供了一套基于Kepler导出能源相关指标的工具，用于支持模型训练、导出、服务和使用。请按照以下步骤开始使用本项目。

## 第一步：了解训练流程

首先需要从[训练流程](./pipeline.md)文档中了解功率模型构建的基本概念。

## 第二步：学习如何使用功率模型

### 选择估算器

---

根据模型格式的不同，有两种使用方式。如果模型格式可以直接在Kepler导出器内处理（如线性回归权重以`json`格式存储），则无需额外配置。

但如果模型是以`zip`归档的通用格式存储，则需要通过环境变量或Kepler配置映射启用估算器边车。

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

静态方式是从`INIT_URL`直接下载模型。可以通过环境变量或`kepler-cfm`配置映射设置。例如：

```bash
export NODE_COMPONENTS_INIT_URL= < 静态URL >
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
        NODE_COMPONENTS_INIT_URL= < 静态URL >
```

v0.7版本提供的静态URL列表可在[此处](https://github.com/sustainable-computing-io/kepler-model-db/tree/main/models/v0.7)查看。

#### 通过服务器API动态获取

动态方式是启用模型服务器自动选择具有最佳准确性且支持当前集群环境的功率模型。同样可以通过环境变量或配置映射设置。

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

更多详情请参阅[Kepler功率估算部署](./power_estimation.md)

## 第三步：学习如何训练功率模型并回馈社区

您可能已经意识到，针对特定机器类型定制功率模型比依赖单一通用模型更为重要。我们热忱欢迎社区贡献，通过模型服务器项目帮助在您的机器上构建替代功率模型。

有关模型训练的详细指南，请参考[模型训练指南](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/model_training)。