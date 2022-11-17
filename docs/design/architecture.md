# Components

## Kepler Exporter
![](https://raw.githubusercontent.com/sustainable-computing-io/kepler/main/doc/kepler-arch.png)

## Kepler Model Server
The main feature of Kepler Model Server is to return a [power estimation model](./power_estimation.md) correponding to the request containing target granularity (node in total, node per each processor component, pod in total, pod per each processor component), available input metrics, model filters such as acccuracy.

In addition, the online-trainer can be deployed as a sidecar container to the server (main container) to execute trainning pipelines and update the model on the fly when power metrics are available.

Check us out on GitHub ➡️ [Kepler Model Server](https://github.com/sustainable-computing-io/kepler-model-server)

## Kepler Estimator Sidecar
Kepler estimator is a client module to kepler model server running as a sidecar of Kepler exporter (main container).

This python will serve a PowerReequest from model package in Kepler exporter as defined in estimator.go via unix domain socket `/tmp/estimator.sock`.

Check us out on GitHub ➡️ [Kepler Estimator](https://github.com/sustainable-computing-io/kepler-estimator)