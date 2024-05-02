# Local cluster setup

Kepler runs on Kubernetes. If you already have access to a cluster, you can skip this section. To deploy a local cluster,
you can use [kind](https://kind.sigs.k8s.io/). `kind` is a tool for running local Kubernetes clusters using Docker container
"nodes". It was primarily designed for testing Kubernetes itself, but may be used for local development or CI.

## Install kind

To install `kind`, please [see the instructions here](https://kind.sigs.k8s.io/docs/user/quick-start/#installation).

We need to configure our cluster to run Kepler. Specifically, we need to mount `/proc` (to expose
information about processes running on the host) and `/usr/src` (to expose kernel headers allowing
dynamic eBPF program compilation - this dependency [might be removed in future releases][1] into the
node containers. Below is a minimal single-node example configuration:

```yaml
$ cat ./local-cluster-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: my-cluster
nodes:
- role: control-plane
  image: kindest/node:v1.27.3@sha256:3966ac761ae0136263ffdb6cfd4db23ef8a83cba8a463690e98317add2c9ba72
  extraMounts:
  - hostPath: /proc
    containerPath: /proc-host
  - hostPath: /usr/src
    containerPath: /usr/src
```

We can then spin up a cluster with either:

```console
export CLUSTER_NAME="my-cluster"  # we can use the --name flag to override the name in our config
kind create cluster --name=$CLUSTER_NAME --config=./local-cluster-config.yaml
```

or simply by running:

```console
make cluster-up
```

Note that `kind` automatically switches your current `kubeconfig` context to the newly created cluster.

[1]: https://github.com/sustainable-computing-io/kepler/issues/716
