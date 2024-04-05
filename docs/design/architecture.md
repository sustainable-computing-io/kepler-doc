# Components

## Kepler Exporter

Kepler Exporter exposes a variety of metrics about the energy consumption of Kubernetes components such as Pods and Nodes.

Monitor container power consumption with the [metrics](metrics.md) made available by the Kepler Exporter.

![Kepler Architecture](https://raw.githubusercontent.com/sustainable-computing-io/kepler/main/doc/kepler-arch.png)

## Kepler Model Server

The main feature of `Kepler Model Server` is to return a [power estimation model](../kepler_model_server/power_estimation.md) corresponding to the request containing target granularity (node in total, node per each processor component, pod in total, pod per each processor component), available input metrics, model filters such as accuracy.

In addition, the online-trainer can be deployed as a sidecar container to the server (main container) to execute training pipelines and update the model on the fly when power metrics are available.

`Kepler Estimator` is a client module to kepler model server running as a sidecar of Kepler Exporter (main container).

This python will serve a PowerRequest from model package in Kepler Exporter as defined in estimator.go via unix domain socket `/tmp/estimator.sock`.

Check us out on GitHub ➡️ [Kepler Model Server](https://github.com/sustainable-computing-io/kepler-model-server)
