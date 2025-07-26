# 组件

## Kepler Exporter

Kepler Exporter 提供了关于 Kubernetes 组件（如 Pod 和节点）能耗的各种指标。

通过 Kepler Exporter 提供的[指标](metrics.md)，监控容器的能耗情况。

![Kepler 架构](https://raw.githubusercontent.com/sustainable-computing-io/kepler/main/doc/kepler-arch.png)

## Kepler Model Server

`Kepler Model Server` 的主要功能是根据请求返回对应的[能耗估算模型](../kepler_model_server/power_estimation.md)，该请求包含目标粒度（节点总体、节点每个处理器组件、Pod 总体、Pod 每个处理器组件）、可用的输入指标以及模型筛选条件（如精确度等）。

此外，在线训练器可以作为服务器（主容器）的边车容器部署，用于在能耗指标可用时执行训练流程并动态更新模型。

`Kepler Estimator` 是 Kepler Model Server 的客户端模块，作为 Kepler Exporter（主容器）的边车运行。

该 Python 程序将通过 Unix 域套接字 `/tmp/estimator.sock` 为 Kepler Exporter 中 estimator.go 定义的模型包提供 PowerRequest 服务。

访问我们的 GitHub ➡️ [Kepler Model Server](https://github.com/sustainable-computing-io/kepler-model-server)