# Kepler Installation
## Requirements
- Kernel 4.18+
- Access to a Kubernetes cluster
- `kubectl` v1.21.0+

## Deploy the Kepler Exporter
Follow the steps below to deploy the Kepler exporter as a Daemonset to run on all Nodes. The following deployment will also create a service listening on port `9102`.

First, fork and clone this repo.

Then, build the manifests file for either VM+Baremetal or Baremetal only with the following `make` command.

```
make build-manifest
```
Manifests will be generated in  `_output/manifests/kubernetes/generated/` by default.

If you are deploying on Baremetal only:
```
kubectl create -f _output/manifests/kubernetes/generated/bm/deployment.yaml
```

If you are deploying on Baremetal and/or VM:
```
kubectl create -f _output/manifests/kubernetes/generated/vm/deployment.yaml
```

## Deploy the Prometheus operator and the whole monitoring stack
If Prometheus is already installed in the cluster, skip this step. Otherwise, follow these steps to install it.

1. Clone the [kube-prometheus](https://github.com/prometheus-operator/kube-prometheus) project to your local folder.
```
# git clone https://github.com/prometheus-operator/kube-prometheus
```

1. Deploy the whole monitoring stack using the config in the `manifests` directory.
Create the namespace and CRDs, and then wait for them to be available before creating the remaining resources
```
# cd kube-prometheus
# kubectl apply --server-side -f manifests/setup
# until kubectl get servicemonitors --all-namespaces ; do date; sleep 1; echo ""; done
# kubectl apply -f manifests/
```

## Configure Prometheus to scrape Kepler-exporter endpoints.
```
# cd ../kepler
# kubectl create -f manifests/kubernetes/keplerExporter-serviceMonitor.yaml
```





