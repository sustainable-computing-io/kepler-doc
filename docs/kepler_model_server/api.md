# Kepler Model Server API
## Getting Powers from Estimator
**module:** estimator (src/estimate/estimator.py)
```
/tmp/estimator.socket
```
Parameters of [PowerRequest](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/estimate/estimator.py)
|key|value|description
|---|---|---|
|metrics|list of string|list of available input features (measured metrics)
|output_type|either of the following values: *AbsPower* (for node-level power model), *DynPower* (for container-level power model)|the requested model type 
|trainer_name (optional)|string|filter model with trainer name.
|filter (optional)|string|expression in the form *attribute1*:*threshold1*; *attribute2*:*threshold2*.

## Getting Power Models from Model Server 
**module:** server (src/server/model_server.py)
```
:8100/model
POST
```

Parameters of [ModelRequest](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/server/model_server.py)
|key|value|description
|---|---|---|
|metrics|list of string|list of available input features (measured metrics)
|output_type|either of the following values: *AbsPower* (for node-level power model), *DynPower* (for container-level power model)|the requested model type 
|weight|boolean|return model weights in json format if true. Otherwise, return model in zip file format.
|trainer_name (optional)|string|filter model with trainer name.
|node_type (optional)|string|filter model with node type.
|filter (optional)|string|expression in the form *attribute1*:*threshold1*; *attribute2*:*threshold2*.

## Offline Trainer
**module:** offline trainer (src/train/offline_trainer.py)
```
:8102/train
POST
```
Parameters of [TrainRequest](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/train/offline_trainer.py)
|key|value|description
|---|---|---|
|name|string|pipeline/model name
|energy_source|valid key in [PowerSourceMap](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/util/train_types.py)|target enery source to train for 
|trainer|TrainAttribute|attributes for training
|prome_response|json|prom response with workload for power model training

- TrainAttribute
    |key|value|description
    |---|---|---|
    |abs_trainers|list of [available trainer class names](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/train/trainer)|trainer classes in the pipeline to train for absolute power
    |dyn_trainers|list of [available trainer class names](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/train/trainer)|trainer classes in the pipeline to train for dynamic power
    |isolator|[valid isolator class name](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/src/train/isolator/)|isolator class of the pipeline to isolate the target data to train for dynamic power
    |isolator_args|dict|mapping between isolator-specific argument name and value


## Posting Model Weights [WIP]
**module:** server (src/server/model_server.py)
```
/metrics
GET
```

## Online Trainer [WIP]
**module:** online trainer (src/train/online_trainer.py)
running as a sidecar to server
```
periodically query prometheus metric server on SAMPLING INTERVAL
```

## Profiler [WIP]
**module:** profiler (src/profile/profiler.py)


