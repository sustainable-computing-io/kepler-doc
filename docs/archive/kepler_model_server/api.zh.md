# Kepler 模型服务器 API

## 从估算器获取功率数据

**模块:** estimator (src/estimate/estimator.py)

```sh
/tmp/estimator.socket
```

### [PowerRequest](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/estimate/estimator.py) 参数

|键|值|描述
|---|-----|-----------
|metrics|字符串列表|可用输入特征列表（测量指标）
|output_type|可选值：*AbsPower*（节点级功耗模型）或 *DynPower*（容器级功耗模型）|请求的模型类型
|trainer_name (可选)|字符串|按训练器名称筛选模型
|filter (可选)|字符串|表达式格式：*属性1*:*阈值1*; *属性2*:*阈值2*

## 从模型服务器获取功率模型

**模块:** server (src/server/model_server.py)

```sh
:8100/model
POST
```

### [ModelRequest](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/server/model_server.py) 参数

|键|值|描述
|---|-----|:------------
|metrics|字符串列表|可用输入特征列表（测量指标）
|output_type|可选值：*AbsPower*（节点级功耗模型）或 *DynPower*（容器级功耗模型）|请求的模型类型
|weight|布尔值|为true时返回json格式的模型权重，否则返回zip文件格式的模型
|trainer_name (可选)|字符串|按训练器名称筛选模型
|node_type (可选)|字符串|按节点类型筛选模型
|filter (可选)|字符串|表达式格式：*属性1*:*阈值1*; *属性2*:*阈值2*

## 离线训练器

**模块:** offline trainer (src/train/offline_trainer.py)

```sh
:8102/train
POST
```

### [TrainRequest](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/train/offline_trainer.py) 参数

|键|值|描述
|---|---|---
|name|字符串|管道/模型名称
|energy_source|[PowerSourceMap](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/util/train_types.py)中的有效键|训练目标能源类型
|trainer|TrainAttribute|训练属性
|prome_response|json|包含功耗模型训练工作负载的prom响应数据

#### 训练属性(TrainAttribute)

|键|值|描述
|---|---|---
|abs_trainers|[可用训练器类名](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/train/trainer)列表|用于训练绝对功耗的管道训练器类
|dyn_trainers|[可用训练器类名](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/train/trainer)列表|用于训练动态功耗的管道训练器类
|isolator|[有效隔离器类名](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/train/isolator/)|用于隔离目标数据以训练动态功耗的管道隔离器类
|isolator_args|字典|隔离器特定参数名与值的映射

## 提交模型权重 [开发中]

**模块:** server (src/server/model_server.py)

```sh
/metrics
GET
```

## 在线训练器 [开发中]

**模块:** online trainer (src/train/online_trainer.py)
作为服务器的sidecar运行

```sh
定期以采样间隔查询prometheus指标服务器
```

## 分析器 [开发中]

**模块:** profiler (src/profile/profiler.py)