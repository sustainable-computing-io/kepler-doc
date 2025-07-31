# 组件

## Kepler Exporter

Kepler Exporter 公开了关于 Kubernetes 组件（如 Pod 和节点）能耗的各种指标。

通过 Kepler Exporter 提供的[指标](metrics.md)监控容器功耗。

![Kepler Architecture](https://raw.githubusercontent.com/sustainable-computing-io/kepler/main/doc/kepler-arch.png)

## Kepler Model Server

`Kepler Model Server` 的主要功能是返回与请求相对应的[功耗估算模型](../kepler_model_server/power_estimation.md)，该请求包含目标粒度（节点总计、节点按每个处理器组件、Pod 总计、Pod 按每个处理器组件）、可用输入指标、模型过滤器（如准确性）。

此外，在线训练器可以作为侧车容器部署到服务器（主容器）中，以执行训练管道并在功耗指标可用时实时更新模型。

`Kepler Estimator` 是 Kepler 模型服务器的客户端模块，作为 Kepler Exporter（主容器）的侧车运行。

此 Python 模块将通过 Unix 域套接字 `/tmp/estimator.sock` 处理来自 Kepler Exporter 中模型包的 PowerRequest，如 estimator.go 中定义的那样。

在 GitHub 上查看我们 ➡️ [Kepler Model Server](https://github.com/sustainable-computing-io/kepler-model-server)
