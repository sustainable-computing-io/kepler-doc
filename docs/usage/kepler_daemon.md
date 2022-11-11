# Kepler DaemonSet Customization
Kepler enables a function to hybrid read environment variable from attributes directly (container.env) and from the ConfigMap. Note that, all steps will be operated by [Kepler Operator](https://github.com/sustainable-computing-io/kepler-operator) if the operator is installed.

To set environments by ConfigMap,

1. Create/Generate ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kepler-cfm
  namespace: kepler-system
data:
  MODEL_SERVER_ENABLE: true
  COUNTER_METRICS: '*'
  CGROUP_METRICS: '*'
  BPF_METRICS: '*'
  # KUBELET_METRICS: ''
  # GPU_METRICS: ''
  PERF_METRICS: '*'
  MODEL_CONFIG: |
    POD_COMPONENT_ESTIMATOR=true
    POD_COMPONENT_INIT_URL=https://raw.githubusercontent.com/sustainable-computing-io/kepler-model-server/main/tests/test_models/DynComponentPower/CgroupOnly/ScikitMixed.zip
```

2. Mount the confimap to DeamonSet
```yaml
  spec:
    containers:
      - name: kepler-exporter
        volumeMounts:
        - name: cfm
          mountPath: /etc/config
          readOnly: true
      volumes:
      - name: cfm
        configMap:
          name: kepler-cfm
```