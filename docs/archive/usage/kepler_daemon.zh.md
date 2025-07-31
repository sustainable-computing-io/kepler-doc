# Kepler DaemonSet 自定义

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

Kepler 启用了一个功能，可以混合从属性直接（container.env）和从 ConfigMap
读取环境变量。请注意，如果安装了操作器，所有步骤都将由 [Kepler Operator](https://github.com/sustainable-computing-io/kepler-operator) 操作。

通过 ConfigMap 设置环境变量：

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

2. 将 ConfigMap 挂载到 DaemonSet：

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
