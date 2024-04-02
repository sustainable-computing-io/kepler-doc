# Configuration

This is a list of configurable values of Kepler System. The configuration can be also applied by defining the following CR spec if Kepler Operator is installed.

|Point of Configuration|Spec|Description|Default|
|---|---|---|---|
|***Kepler CR*** (single item: default)||||
|Kepler DaemonSet Deployment|daemon.exporter.image|Kepler main image|quay.io/sustainable_computing_io/kepler:latest|
|Kepler DaemonSet Deployment|daemon.exporter.port|Metric exporter port|9102|
|Kepler DaemonSet Deployment|daemon.estimator-sidecar.enabled|[Kepler Estimator Sidecar](./../kepler_model_server/get_started.md#step-3-learn-how-to-use-the-power-model) patch|false|
|Kepler DaemonSet Deployment|daemon.estimator-sidecar.image|Kepler estimator sidecar image|-|
|Kepler DaemonSet Deployment|daemon.estimator-sidecar.mnt-path|Mount path between main container and the sidecar for unix domain socket|/tmp|
|Kepler DaemonSet Environment (METRIC_PATH)|daemon.exporter.path|Path to export metrics|/metrics|
|Kepler DaemonSet Environment (MODEL_SERVER_ENABLE)|model-server.enaled|[Kepler Model Server Pod](./../kepler_model_server/get_started.md#step-2-learn-how-to-obtain-power-model) connection|false|
|**model-server.enabled**||||
|Model Server Pod Pod Environment (MODEL_SERVER_PORT)|model-server.port|Model serving port of model server|8100|
|Model Server Pod Pod Environment (PROM_SERVER)|model-server.prom|Endpoint to Prometheus metric server |`http://prometheus-k8s.monitoring.svc.cluster.local:9090`|
|Model Server Pod Pod Environment (MODEL_PATH)|model-server.model-path|Path to keep models|models|
|Kepler DaemonSet Environment (MODEL_SERVER_ENDPOINT)|daemon.model-server|Endpoint to server container of model server|`http://kepler-model-server.monitoring.cluster.local:[model-server.port]/model`|
|Model Server Pod Deployment|model-server.trainer|Model online trainer patch|false|
|**model-server.trainer**||||
|Model Server Pod Environment (PROM_QUERY_INTERVAL)|model-server.prom_interval|Interval to execute trainning pipelines in seconds|20|
|Model Server Pod Environment (PROM_QUERY_STEP)|model-server.prom-step|Step of query data point in trainning pipelines in seconds|3|
|Model Server Pod Environment (PROM_HEADERS)|model-server.prom-header|For specify required header (such as authentication)|-|
|Model Server Pod Environment (PROM_SSL_DISABLE)|model-server.prom-ssl|Disable ssl in Prometheus connection|true|
|Model Server Pod Environment (INITIAL_MODELS_LOC)|model-server.init-loc|Root URL of offline models to use as initial models|`https://raw.githubusercontent.com/sustainable-computing-io/kepler-model-server/main/tests/test_models`|
|Model Server Pod Environment (INITIAL_MODEL_NAMES.[`MODEL_TYPE`])|model-server.[`MODEL_TYPE`]|Name of default pipeline for each model type|-|
|***CollectMetric CR*** (single item: default)||||
|Kepler DaemonSet Environment (COUNTER_METRICS)|counter|List of performance metrics to enable from counter source| * (enable all available metrics from counter source)|
|Kepler DaemonSet Environment (CGROUP_METRICS)|cgroup|List of performance metrics to enable from cgroup source| * (enable all available metrics from cgroup source)|
|Kepler DaemonSet Environment (BPF_METRICS)|bpf|List of performance metrics to enable from bpf (aka. ebpf) source| * (enable all available metrics from bpf source)|
|Kepler DaemonSet Environment (GPU_METRICS)|gpu|List of performance metrics to enable from gpu source| * (enable all available metrics from gpu source)|
|***ExportMetric CR*** (single item: default)||||
|Kepler DaemonSet Environment (PERF_METRICS)|perf|List of performance metrics to export | * (enable all collected performance metrics)|
|Kepler DaemonSet Environment (EXPORT_NODE_TOTAL_POWER)|node_total_power|Toggle whether to export node total power| true|
|Kepler DaemonSet Environment (EXPORT_NODE_COMPONENT_POWERS)|node_component_powers|Toggle whether to export node powers by components| true|
|Kepler DaemonSet Environment (EXPORT_POD_TOTAL_POWER)|pod_total_power|Toggle whether to export pod total power| true|
|Kepler DaemonSet Environment (EXPORT_POD_COMPONENT_POWERS)|pod_component_powers|Toggle whether to export pod powers by components| true|
|***EstimatorConfig CR*** (multiple items: node-total-power, node-component-powers, pod-total-power, pod-component-powers)||||
|Kepler DaemonSet Environment (MODEL_CONFIG.[`MODEL_ITEM`]_ESTIMATOR)|use-sidecar|Toggle whether to use estimator sidecar for power estimation|false|
|Kepler DaemonSet Environment (MODEL_CONFIG.[`MODEL_ITEM`]_MODEL)|fixed-model|Specify model name| (auto-selected)|
|Kepler DaemonSet Environment (MODEL_CONFIG.[`MODEL_ITEM`]_FILTERS)|filters|Specify model filter conditions in string|  (auto-selected)|
|Kepler DaemonSet Environment (MODEL_CONFIG.[`MODEL_ITEM`]_INIT_URL)|init-url|URL to initial model location| -|
|***RatioConfig CR*** (single items: default)||||
|Kepler DaemonSet Environment (CORE_USAGE_METRIC)|core_metric|Specify metric for compute core (mostly cpu) component of pod power by ratio modeling|cpu_instr|
|Kepler DaemonSet Environment (DRAM_USAGE_METRIC)|dram_metric|Specify metric for computing dram component of pod power by ratio modeling|cache_miss|
|Kepler DaemonSet Environment (UNCORE_USAGE_METRIC)|uncore_metric|Specify metric for computing uncore component of pod power by ratio modeling|(evenly divided)|
|Kepler DaemonSet Environment (GENERAL_USAGE_METRIC)|general_metric|Specify metric for computing uncategorized component (pkg-core-uncore) of pod power by ratio modeling|cpu_instr|
|Kepler DaemonSet Environment (GPU_USAGE_METRIC)|core_metric|Specify metric for computing gpu component of pod power by ratio modeling|-|

**Remarks:**

- [`MODEL_ITEM`] can be either of the following values corresponding to item names: `NODE_TOTAL`, `NODE_COMPONENT`, `POD_TOTAL`, `POD_COMPONENTS`.
- [`MODEL_TYPE`] is a concatenation of [`MODEL_ITEM`] and [`OUTPUT_FORMAT`] which can be either `POWER` for archived model or `MODEL_WEIGHT` for weights in json.

  For example:

  - `NODE_TOTAL_POWER`: archived model to estimate node total power used by estimator sidecar
  - `POD_COMPONENTS_MODEL_WEIGHT`: model weight to estimate pod component powers used by linear regressor embedded in Kepler main component.
