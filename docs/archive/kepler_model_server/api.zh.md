# Kepler 模型服务器 API

## 从估算器获取功率

**模块：** estimator (src/estimate/estimator.py)

```sh
/tmp/estimator.socket
```

### [PowerRequest](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/estimate/estimator.py) 的参数

|键|值|描述
|---|-----|-----------
|metrics|字符串列表|可用输入特征（测量指标）列表
|output_type|以下值之一：*AbsPower*（用于节点级功率模型）、*DynPower*（用于容器级功率模型）|请求的模型类型
|trainer_name（可选）|字符串|按训练器名称过滤模型
|filter（可选）|字符串|形式为 *attribute1*:*threshold1*; *attribute2*:*threshold2* 的表达式

## 从模型服务器获取功率模型

**模块：** server (src/server/model_server.py)

```sh
:8100/model
POST
```

### [ModelRequest](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/server/model_server.py) 的参数

|键|值|描述
|---|-----|:------------
|metrics|字符串列表|可用输入特征（测量指标）列表
|output_type|以下值之一：*AbsPower*（用于节点级功率模型）、*DynPower*（用于容器级功率模型）|请求的模型类型
|weight|布尔值|如果为 true，以 json 格式返回模型权重。否则，以 zip 文件格式返回模型。
|trainer_name（可选）|字符串|按训练器名称过滤模型。
|node_type（可选）|字符串|按节点类型过滤模型。
|filter（可选）|字符串|形式为 *attribute1*:*threshold1*; *attribute2*:*threshold2* 的表达式。

## 离线训练器

**模块：** offline trainer (src/train/offline_trainer.py)

```sh
:8102/train
POST
```

### [TrainRequest](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/train/offline_trainer.py) 的参数

|键|值|描述
|---|---|---
|name|字符串|管道/模型名称
|energy_source|[PowerSourceMap](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/util/train_types.py) 中的有效键|要训练的目标能源来源
|trainer|TrainAttribute|训练属性
|prome_response|json|包含用于功率模型训练的工作负载的 prom 响应

#### TrainAttribute

|键|值|描述
|---|---|---
|abs_trainers|[可用训练器类名](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/train/trainer)列表|管道中用于训练绝对功率的训练器类
|dyn_trainers|[可用训练器类名](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/train/trainer)列表|管道中用于训练动态功率的训练器类
|isolator|[有效隔离器类名](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/train/isolator/)|管道的隔离器类，用于隔离目标数据以训练动态功率
|isolator_args|字典|隔离器特定参数名称和值之间的映射

## 发布模型权重 [进行中]

**模块：** server (src/server/model_server.py)

```sh
/metrics
GET
```

## 在线训练器 [进行中]

**模块：** online trainer (src/train/online_trainer.py)
作为服务器的 sidecar 运行

```sh
在采样间隔上定期查询 prometheus 指标服务器
```

## 分析器 [进行中]

**模块：** profiler (src/profile/profiler.py)
