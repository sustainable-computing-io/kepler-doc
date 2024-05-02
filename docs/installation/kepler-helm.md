# Deploy using Helm Chart

The Kepler Helm Chart is available on
[GitHub](https://github.com/sustainable-computing-io/kepler-helm-chart/tree/main)
and [ArtifactHub](https://artifacthub.io/packages/helm/kepler/kepler)

## Install Helm


[Helm](https://helm.sh) must be installed to use the charts.
Please refer to Helm's [documentation](https://helm.sh/docs/) to get started.

## Prometheus Setup

The Kepler Exporter requires the [Prometheus Node
Exporter](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus-node-exporter)
to be installed. We recommend the [Kube Prometheus
Stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)
helm chart, which includes the Node Exporter, Grafana and other helpful stuff to
provide easy to operate end-to-end Kubernetes cluster monitoring with Prometheus
using the Prometheus Operator.

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
    --namespace monitoring \
    --create-namespace \
    --wait
```


## Add the Kepler Helm repo

```bash
helm repo add kepler https://sustainable-computing-io.github.io/kepler-helm-chart
helm repo update
```

You can see the latest version by using the following command:

```bash
helm search repo kepler
```

If you would like to test and look at the manifest files before deploying you can run:

```bash
helm install kepler kepler/kepler --namespace kepler --create-namespace --dry-run --devel
```

## Install Kepler

For Prometheus to be able to discover the metrics exported by Kepler, the
`serviceMonitor` needs to be enabled and labeled with the release name of your
Prometheus install. In our installation we called our kube-prometheus-stack install `prometheus`:

```bash
helm install kepler kepler/kepler \
    --namespace kepler \
    --create-namespace \
    --set serviceMonitor.enabled=true \
    --set serviceMonitor.labels.release=prometheus \
```

Alternatively, you can also override the
[values.yaml](https://github.com/sustainable-computing-io/kepler-helm-chart/blob/main/chart/kepler/values.yaml)
file to set these and the following values:

```bash
helm install kepler kepler/kepler --values values.yaml --namespace kepler --create-namespace
```

The following table lists the configurable parameters for this chart and their default values.

Parameter|Description| Default
---|---|---
global.namespace| Kubernetes namespace for Kepler |kepler
image.repository|Repository for Kepler Image| quay.io/sustainable\_computing\_io/kepler
image.pullPolicy|Pull policy for Kepler|Always
image.tag|Image tag for Kepler Image |latest
serviceAccount.name|Service account name for Kepler|kepler-sa
service.type|Kepler service type|ClusterIP
service.port|Kepler service exposed port|9102

## Post Install

After Installation you can wait for Kepler to get ready:

```bash
KPLR_POD=$(
    kubectl get pod \
        -l app.kubernetes.io/name=kepler \
        -o jsonpath="{.items[0].metadata.name}" \
        -n kepler
)
kubectl wait --for=condition=Ready pod $KPLR_POD --timeout=-1s -n kepler
```

and add the [Kepler
dashboard](https://github.com/sustainable-computing-io/kepler/blob/main/grafana-dashboards/Kepler-Exporter.json)
to Grafana:

```bash
GF_POD=$(
    kubectl get pod \
        -n monitoring \
        -l app.kubernetes.io/name=grafana \
        -o jsonpath="{.items[0].metadata.name}"
)
kubectl cp kepler_dashboard.json monitoring/$GF_POD:/tmp/dashboards/kepler_dashboard.json
```

## Uninstall Kepler

To uninstall this chart, use the following steps

```bash
helm delete kepler --namespace kepler
```
