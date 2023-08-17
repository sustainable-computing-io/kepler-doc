# 组件

## Kepler Exporter
Kepler Exporter公开了有关Kubernetes组件（如Pods和Nodes）能耗的各种指标。

请点击链接查看相关能耗[指标/metrics](metrics.md)的定义。

![](https://raw.githubusercontent.com/sustainable-computing-io/kepler/main/doc/kepler-arch.png)

## Kepler Model Server
Kepler Model Server主要提供[能耗预估模型](../kepler_model_server/power_estimation.md)，该模型支持对各种粒度的（如节点数，节点CPU数，Pod数，Pod进程数）的请求，并返回指标，精准性模型过滤器。

另外，在online训练模式，Kepler Model Server可以作为边车部署。并且执行训练相关流程，实时更新模型。

Kepler Estimator作为Kepler Exporter的边车部署，将会以客户端模式运行，访问kepler model server，请求模型。

Kepler estimator与Kepler Exporter通过socket的方式（`/tmp/estimator.sock`）进行连接。相关的代码在Kepler Exporter的`estimator.go`文件中有定义和描述。

项目地址 ➡️ [Kepler Model Server](https://github.com/sustainable-computing-io/kepler-model-server)