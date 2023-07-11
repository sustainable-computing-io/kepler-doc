# Kepler Operator on Kind

## Getting Started

You’ll need a Kubernetes cluster to run against. You can use KIND to get a local cluster for testing, or run against a remote cluster. Note: Your controller will automatically use the current context in your kubeconfig file (i.e. whatever cluster kubectl cluster-info shows).

### To run a kind cluster locally

``` sh
make cluster-up CLUSTER_PROVIDER='kind' CI_DEPLOY=true GRAFANA_ENABLE=true
```

### To run kepler-operator locally on the cluster
You can use the image from quay.io to deploy kepler-operator.

```sh
make deploy IMG=quay.io/sustainable_computing_io/kepler-operator:latest
kubectl apply -k config/samples/
```

### Uninstall the operator
To delete the CRDs from the cluster:
```sh
make undeploy
```


To run Kepler operator on a kind cluster [follow](https://github.com/sustainable-computing-io/kepler-operator#getting-started) 