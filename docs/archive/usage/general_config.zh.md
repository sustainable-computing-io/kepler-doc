# 配置

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

这是 Kepler 系统可配置值的列表。如果已安装 Kepler Operator，也可以通过定义以下 CR 规范来应用配置。

|配置点|规范|描述|默认值|
|---|---|---|---|
|***Kepler CR***（单项：default）||||
|Kepler DaemonSet 部署|daemon.exporter.image|Kepler 主镜像|quay.io/sustainable_computing_io/kepler:latest|
|Kepler DaemonSet 部署|daemon.exporter.port|指标导出器端口|9102|
|Kepler DaemonSet 部署|daemon.estimator-sidecar.enabled|[Kepler Estimator Sidecar](./../kepler_model_server/get_started.zh.md#step-3-learn-how-to-use-the-power-model) 补丁|false|
|Kepler DaemonSet 部署|daemon.estimator-sidecar.image|Kepler 估算器边车镜像|-|
|Kepler DaemonSet 部署|daemon.estimator-sidecar.mnt-path|主容器和边车之间用于 unix 域套接字的挂载路径|/tmp|
|Kepler DaemonSet 环境变量（METRIC_PATH）|daemon.exporter.path|导出指标的路径|/metrics|
|Kepler DaemonSet 环境变量（MODEL_SERVER_ENABLE）|model-server.enabled|[Kepler Model Server Pod](./../kepler_model_server/get_started.zh.md#step-2-learn-how-to-obtain-power-model) 连接|false|
|**model-server.enabled**||||
|Model Server Pod 环境变量（MODEL_SERVER_PORT）|model-server.port|模型服务器的模型服务端口|8100|
|Model Server Pod 环境变量（PROM_SERVER）|model-server.prom|Prometheus 指标服务器的端点|`http://prometheus-k8s.monitoring.svc.cluster.local:9090`|
|Model Server Pod 环境变量（MODEL_PATH）|model-server.model-path|保存模型的路径|models|
|Kepler DaemonSet 环境变量（MODEL_SERVER_ENDPOINT）|daemon.model-server|模型服务器的服务容器端点|`http://kepler-model-server.monitoring.cluster.local:[model-server.port]/model`|
|Model Server Pod 部署|model-server.trainer|模型在线训练器补丁|false|
|**model-server.trainer**||||
|Model Server Pod 环境变量（PROM_QUERY_INTERVAL）|model-server.prom_interval|执行训练管道的间隔（秒）|20|
|Model Server Pod 环境变量（PROM_QUERY_STEP）|model-server.prom-step|训练管道中查询数据点的步长（秒）|3|
|Model Server Pod 环境变量（PROM_HEADERS）|model-server.prom-header|用于指定所需标头（如身份验证）|-|
|Model Server Pod 环境变量（PROM_SSL_DISABLE）|model-server.prom-ssl|禁用 Prometheus 连接中的 ssl|true|
|Model Server Pod 环境变量（INITIAL_MODELS_LOC）|model-server.init-loc|用作初始模型的离线模型的根 URL|`https://raw.githubusercontent.com/sustainable-computing-io/kepler-model-server/main/tests/test_models`|
|Model Server Pod 环境变量（INITIAL_MODEL_NAMES.[`MODEL_TYPE`]）|model-server.[`MODEL_TYPE`]|每种模型类型的默认管道名称|-|
|***CollectMetric CR***（单项：default）||||
|Kepler DaemonSet 环境变量（COUNTER_METRICS）|counter|从计数器源启用的性能指标列表|*（启用计数器源的所有可用指标）|
|Kepler DaemonSet 环境变量（BPF_METRICS）|bpf|从 bpf（即 eBPF）源启用的性能指标列表|*（启用 bpf 源的所有可用指标）|
|Kepler DaemonSet 环境变量（GPU_METRICS）|gpu|从 gpu 源启用的性能指标列表|*（启用 gpu 源的所有可用指标）|
|***ExportMetric CR***（单项：default）||||
|Kepler DaemonSet 环境变量（PERF_METRICS）|perf|要导出的性能指标列表|*（启用所有收集的性能指标）|
|Kepler DaemonSet 环境变量（EXPORT_NODE_TOTAL_POWER）|node_total_power|切换是否导出节点总功率|true|
|Kepler DaemonSet 环境变量（EXPORT_NODE_COMPONENT_POWERS）|node_component_powers|切换是否按组件导出节点功率|true|
|Kepler DaemonSet 环境变量（EXPORT_POD_TOTAL_POWER）|pod_total_power|切换是否导出 Pod 总功率|true|
|Kepler DaemonSet 环境变量（EXPORT_POD_COMPONENT_POWERS）|pod_component_powers|切换是否按组件导出 Pod 功率|true|
|***EstimatorConfig CR***（多项：node-total-power、node-component-powers、pod-total-power、pod-component-powers）||||
|Kepler DaemonSet 环境变量（MODEL_CONFIG.[`MODEL_ITEM`]_ESTIMATOR）|use-sidecar|切换是否使用估算器边车进行功率估算|false|
|Kepler DaemonSet 环境变量（MODEL_CONFIG.[`MODEL_ITEM`]_MODEL）|fixed-model|指定模型名称|（自动选择）|
|Kepler DaemonSet 环境变量（MODEL_CONFIG.[`MODEL_ITEM`]_FILTERS）|filters|以字符串形式指定模型过滤条件|（自动选择）|
|Kepler DaemonSet 环境变量（MODEL_CONFIG.[`MODEL_ITEM`]_INIT_URL）|init-url|初始模型位置的 URL|-|
|***RatioConfig CR***（单项：default）||||
|Kepler DaemonSet 环境变量（CORE_USAGE_METRIC）|core_metric|通过比例建模指定计算核心（主要是 cpu）组件的 Pod 功率指标|cpu_instr|
|Kepler DaemonSet 环境变量（DRAM_USAGE_METRIC）|dram_metric|通过比例建模指定计算 dram 组件的 Pod 功率指标|cache_miss|
|Kepler DaemonSet 环境变量（UNCORE_USAGE_METRIC）|uncore_metric|通过比例建模指定计算非内核组件的 Pod 功率指标|（平均分配）|
|Kepler DaemonSet 环境变量（GENERAL_USAGE_METRIC）|general_metric|通过比例建模指定计算未分类组件（pkg-core-uncore）的 Pod 功率指标|cpu_instr|
|Kepler DaemonSet 环境变量（GPU_USAGE_METRIC）|core_metric|通过比例建模指定计算 gpu 组件的 Pod 功率指标|-|

**备注：**

- [`MODEL_ITEM`] 可以是以下与项目名称对应的值之一：`NODE_TOTAL`、`NODE_COMPONENT`、`POD_TOTAL`、`POD_COMPONENTS`。
- [`MODEL_TYPE`] 是 [`MODEL_ITEM`] 和 [`OUTPUT_FORMAT`] 的连接，可以是用于存档模型的 `POWER` 或用于 json 中权重的 `MODEL_WEIGHT`。

  例如：

  - `NODE_TOTAL_POWER`：估算器边车用于估算节点总功率的存档模型
  - `POD_COMPONENTS_MODEL_WEIGHT`：Kepler 主组件中嵌入的线性回归器用于估算 Pod 组件功率的模型权重。
