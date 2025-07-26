# Kepler DaemonSet 自定义配置

Kepler 提供了一项功能，可以混合读取来自容器属性（container.env）和 ConfigMap 的环境变量。请注意，如果已安装 [Kepler Operator](https://github.com/sustainable-computing-io/kepler-operator)，所有步骤将由该 Operator 自动执行。

通过 ConfigMap 设置环境变量的步骤：

1. 创建/生成 ConfigMap

    ```yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: kepler-cfm
      namespace: kepler-system
    data:
      MODEL_SERVER_ENABLE: true
      COUNTER_METRICS: '*'
      BPF_METRICS: '*'
      # KUBELET_METRICS: ''
      # GPU_METRICS: ''
      PERF_METRICS: '*'
      MODEL_CONFIG: |
        POD_COMPONENT_ESTIMATOR=true
        POD_COMPONENT_INIT_URL=https://raw.githubusercontent.com/sustainable-computing-io/kepler-model-server/main/tests/test_models/DynComponentPower/CgroupOnly/ScikitMixed.zip
    ```

2. 将 ConfigMap 挂载到 DaemonSet:

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