# 使用 Helm Chart 部署

Kepler Helm Chart 可在 [GitHub](https://github.com/sustainable-computing-io/kepler-helm-chart/tree/main) 和 [ArtifactHub](https://artifacthub.io/packages/helm/kepler/kepler) 上找到。

## 安装 Helm

必须安装 [Helm](https://helm.sh) 才能使用图表。
请参阅 Helm 的[文档](https://helm.sh/docs/)以开始使用。

## Prometheus 设置

Kepler 导出器需要已安装 [Prometheus节点导出器](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus-node-exporter) 。我们推荐使用 [Kube Prometheus Stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack) Helm 图表，其中包括 Node Exporter，Grafana 和其他有用的东西，以便轻松操作利用 Prometheus 进行端到端的 Kubernetes 集群监控，使用 Prometheus 运营商。

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \\
    --namespace monitoring \\
    --create-namespace \\
    --wait
```

## 添加 Kepler Helm 仓库

```bash
helm repo add kepler https://sustainable-computing-io.github.io/kepler-helm-chart
helm repo update
```

您可以使用以下命令查看最新版本：

```bash
helm search repo kepler
```

如果您想在部署前测试并查看清单文件，您可以运行：

```bash
helm install kepler kepler/kepler --namespace kepler --create-namespace --dry-run --devel
```

## 安装 Kepler

为了让 Prometheus 能够发现 Kepler 导出的指标，需要启用 `serviceMonitor` 并与您的 Prometheus 安装的发布名称标记。在我们的安装中，我们将 kube-prometheus-stack 安装命名为 `prometheus`：

```bash
helm install kepler kepler/kepler \\
    --namespace kepler \\
    --create-namespace \\
    --set serviceMonitor.enabled=true \\
    --set serviceMonitor.labels.release=prometheus \\
```

或者，您也可以覆盖 [values.yaml](https://github.com/sustainable-computing-io/kepler-helm-chart/blob/main/chart/kepler/values.yaml) 文件来设置这些和以下值:

```bash
helm install kepler kepler/kepler --values values.yaml --namespace kepler --create-namespace
```

以下表格列出了此图表的可配置参数及其默认值。

参数| 描述 | 默认值
---|---|---
global.namespace| Kepler的Kubernetes命名空间 |kepler
image.repository|Kepler Image的存储库| quay.io/sustainable\\_computing\\_io/kepler
image.pullPolicy|Kepler的拉取策略|总是
image.tag|Kepler图像的图像标签|最新
serviceAccount.name|Kepler的服务帐户名称|kepler-sa
service.type|Kepler服务类型|ClusterIP
service.port|Kepler暴露的服务端口|9102

## 安装后

安装后，您可以等待 Kepler 准备就绪：

```bash
KPLR_POD=$(
    kubectl get pod \\
        -l app.kubernetes.io/name=kepler \\
        -o jsonpath=\"{.items[0].metadata.name}\" \\
        -n kepler
)
kubectl wait --for=condition=Ready pod $KPLR_POD --timeout=-1s -n kepler
```

并将 [Kepler仪表盘](https://github.com/sustainable-computing-io/kepler/blob/main/grafana-dashboards/Kepler-Exporter.json) 添加到 Grafana：

```bash
GF_POD=$(
    kubectl get pod \\
        -n monitoring \\
        -l app.kubernetes.io/name=grafana \\
        -o jsonpath=\"{.items[0].metadata.name}\"
)
kubectl cp kepler_dashboard.json monitoring/$GF_POD:/tmp/dashboards/kepler_dashboard.json
```

## 卸载 Kepler
要卸载此图表，请使用以下步骤

```bash
helm delete kepler --namespace kepler
```
