# Deploy using Helm Chart

The Kepler Helm Chart is available on [GitHub](https://github.com/sustainable-computing-io/kepler-helm-chart/tree/main) and [ArtifactHub](https://artifacthub.io/packages/helm/kepler/kepler)

## Install Helm

For Installation [Helm](https://helm.sh) must be installed to use the charts.
Please refer to Helm's [documentation](https://helm.sh/docs/) to get started.

## Add the Kepler Helm repo

```bash
helm repo add kepler https://sustainable-computing-io.github.io/kepler-helm-chart
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

To install run the following:

```bash
helm install kepler kepler/kepler --namespace kepler --create-namespace
```

>You may want to override [values.yaml](https://github.com/sustainable-computing-io/kepler-helm-chart/blob/main/chart/kepler/values.yaml) file use the following command.

```bash
helm install kepler kepler/kepler --values values.yaml --namespace kepler --create-namespace
```

The following table lists the configurable parameters for this chart and their default values.

Parameter|Description| Default
---|---|---
global.namespace| Kubernetes namespace for kepler |kepler
image.repository|Repository for Kepler Image| quay.io/sustainable\_computing\_io/kepler
image.pullPolicy|Pull policy for Kepler|Always
image.tag|Image tag for Kepler Image |latest
serviceAccount.name|Service account name for Kepler|kepler-sa
service.type|Kepler service type|ClusterIP
service.port|Kepler service exposed port|9102

## Uninstall Kepler

To uninstall this chart, use the following steps

```bash
helm delete kepler --namespace kepler
```
