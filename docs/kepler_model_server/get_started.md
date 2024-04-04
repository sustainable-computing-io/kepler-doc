
# Get Started with Kepler Model Server

Model server project facilitates tools for power model training, exporting, serving, and utilizing based on Kepler-exporting energy-related metrics. Check the following steps to get started with the project.

## Step 1: Learn about Pipeline

The first step is to understand about power model building concept from [training pipeline.](./pipeline.md)

## Step 2: Learn how to use the power model

### Select estimator

---

There are two ways to use the models regarding the model format. If the model format can be processed directly inside the Kepler exporter such as Linear Regression weight in `json` format. There is no extra cofiguration.

However, if the model is in the general format archived in `zip`, It is needed to enable the estimator sidecar via environment variable or Kepler config map.

```bash
export NODE_COMPONENTS_ESTIMATOR=true
```

or

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

### Select power model
---

There are two ways to obtain power model: static and dynamic.

#### Static configuration

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
namespace: kepler
data:
    MODEL_CONFIG: |
        NODE_COMPONENTS_INIT_URL= < Static URL >
```

The static URL from provided pipeline v0.7 are listed [here](https://github.com/sustainable-computing-io/kepler-model-db/tree/main/models/v0.7).

#### Dynamic via server API

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
namespace: kepler
data:
    MODEL_CONFIG: |
        MODEL_SERVER_ENABLE: "true"
```

See more in [Kepler Power Estimation Deployment](./power_estimation.md)

## Step 3: Learn how to train the power model and give back to the community

As you may be aware, it's essential to tailor power models to specific machine types rather than relying on a single generic model. We eagerly welcome contributions from the community to help build alternative power models on your machine through the model server project.

For detailed guidance on model training, please refer to our model training guidelines [here](https://github.com/sustainable-computing-io/kepler-model-server/tree/main/model_training).
