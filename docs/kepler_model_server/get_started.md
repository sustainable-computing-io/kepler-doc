# Get Started with Kepler Model Server
## Step 1: [Learn about Pipeline](./pipeline.md)

## Step 2: Learn how to obtain power model
There are two ways to obtain power model: static and dynamic. 

### Static configuration
A static way is to download the model directly from `INIT_URL`. It can be set via environment variable directly or via `kepler-cfm` Kepler config map. For example, 

```bash
export NODE_COMPONENTS_INIT_URL= < Static URL >
```

or

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
name: kepler-cfm
namespace: system
data:
    MODEL_CONFIG: |
        NODE_COMPONENTS_INIT_URL= < Static URL >
```

### Dynamic via server API
A dynamic way is to enable the model server to auto select the power model which has the best accuracy and supported the running cluster environment. Similarly, It can be set via the environment variable or set it via Kepler config map.

```bash
export MODEL_SERVER_ENABLE=true
```

or

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
name: kepler-cfm
namespace: system
data:
    MODEL_CONFIG: |
        MODEL_SERVER_ENABLE: "true"
```

## Step 3: Learn how to use the power model

There are two ways to use the models regarding the model format. If the model format can be processed directly inside the Kepler exporter such as Linear Regression weight in `json` format. There is no extra cofiguration. However, if the model is in the general format archived in `zip`, It is needed to enable the estimator sidecar via environment variable or Kepler config map. 

```bash
export NODE_COMPONENTS_ESTIMATOR=true
```

or

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
name: kepler-cfm
namespace: system
data:
    MODEL_CONFIG: |
        NODE_COMPONENTS_ESTIMATOR=true
```

See more in [Kepler Power Estimation Deployment](./power_estimation.md)

## Step 4: [Learn how to train the power model and give back to the community](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/model_training)