# Model Server Customization
Note that, all steps will be operated by [Kepler Operator](https://github.com/sustainable-computing-io/kepler-operator) if the operator is installed.

To set environments by ConfigMap,

1. Create/Generate ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kepler-model-server-cfm
  namespace: kepler-system
data:
  MODEL_PATH: models
  PROM_SERVER: 'http://prometheus-k8s.monitoring.svc.cluster.local:9090'
  PROM_QUERY_INTERVAL: '20'
  PROM_QUERY_STEP: '3'
  PROM_HEADERS: ''
  PROM_SSL_DISABLE: 'true'
  INITIAL_MODELS_LOC: https://raw.githubusercontent.com/sustainable-computing-io/kepler-model-server/main/tests/test_models
  INITIAL_MODEL_NAMES: |
    NODE_COMPONENTS_MODEL_WEIGHT=KerasCompWeightFullPipeline
    NODE_COMPONENTS_POWER=KerasCompFullPipeline
    POD_COMPONENTS_POWER=ScikitMixed
```

2. Mount the confimap to DeamonSet
```yaml
  spec:
    containers:
      - name: server-api
        volumeMounts:
        - name: cfm
          mountPath: /etc/config
          readOnly: true
      volumes:
      - name: cfm
        configMap:
          name: kepler-model-server-cfm
```