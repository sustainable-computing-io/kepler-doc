# 使用 Helm Chart 部署

Kepler Helm Chart 已发布在  
[GitHub](https://github.com/sustainable-computing-io/kepler-helm-chart/tree/main)  
和 [ArtifactHub](https://artifacthub.io/packages/helm/kepler/kepler)

## 安装 Helm

使用本 Chart 前需先安装 [Helm](https://helm.sh)  
请参考 Helm 官方[文档](https://helm.sh/docs/) 完成安装

## Prometheus 配置

Kepler Exporter 需要依赖 [Prometheus Node Exporter](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus-node-exporter)  
推荐使用 [Kube Prometheus Stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack) Helm Chart，该套件包含：

- Node Exporter  
- Grafana  
- Prometheus Operator  
等组件，可快速搭建完整的 Kubernetes 集群监控方案

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
    --namespace monitoring \
    --create-namespace \
    --wait
```

## 添加 Kepler Helm 仓库

```bash
helm repo add kepler https://sustainable-computing-io.github.io/kepler-helm-chart
helm repo update
```

查看最新版本：

```bash
helm search repo kepler
```

如需在部署前测试和检查清单文件：

```bash
helm install kepler kepler/kepler --namespace kepler --create-namespace --dry-run --devel
```

## 安装 Kepler

为了让 Prometheus 能自动发现 Kepler 导出的指标，需要启用 `serviceMonitor` 并标注 Prometheus 发行版名称（本例中 Prometheus 发行版命名为 `prometheus`）：

```bash
helm install kepler kepler/kepler \
    --namespace kepler \
    --create-namespace \
    --set serviceMonitor.enabled=true \
    --set serviceMonitor.labels.release=prometheus \
```

也可以通过覆盖 [values.yaml](https://github.com/sustainable-computing-io/kepler-helm-chart/blob/main/chart/kepler/values.yaml) 文件进行配置：

```bash
helm install kepler kepler/kepler --values values.yaml --namespace kepler --create-namespace
```

可配置参数及默认值：

参数 | 描述 | 默认值
---|---|---
global.namespace | Kubernetes 命名空间 | kepler
image.repository | 镜像仓库 | quay.io/sustainable\_computing\_io/kepler
image.pullPolicy | 镜像拉取策略 | Always
image.tag | 镜像标签 | latest
serviceAccount.name | 服务账号名称 | kepler-sa
service.type | 服务类型 | ClusterIP
service.port | 服务暴露端口 | 9102

## 安装后操作

等待 Kepler 就绪：

```bash
KPLR_POD=$(
    kubectl get pod \
        -l app.kubernetes.io/name=kepler \
        -o jsonpath="{.items[0].metadata.name}" \
        -n kepler
)
kubectl wait --for=condition=Ready pod $KPLR_POD --timeout=-1s -n kepler
```

添加 [Kepler 仪表盘](https://github.com/sustainable-computing-io/kepler/blob/main/grafana-dashboards/Kepler-Exporter.json) 到 Grafana：

```bash
GF_POD=$(
    kubectl get pod \
        -n monitoring \
        -l app.kubernetes.io/name=grafana \
        -o jsonpath="{.items[0].metadata.name}"
)
kubectl cp kepler_dashboard.json monitoring/$GF_POD:/tmp/dashboards/kepler_dashboard.json
```

## 卸载 Kepler

执行以下命令卸载：

```bash
helm delete kepler --namespace kepler
```