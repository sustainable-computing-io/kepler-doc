# 通过Helm Chart部署kepler

Kepler的Helm Chart目前在[GitHub](https://github.com/sustainable-computing-io/kepler-helm-chart/tree/main)和[ArtifactHub](https://artifacthub.io/packages/helm/kepler/kepler)上可用了。

## 安装Helm
作为准备工作您必须先安装[Helm](https://helm.sh)才可以使用Helm Chart来安装kepler。
您可以参考Helm的[文档](https://helm.sh/docs/)来进行安装。


## 添加Kepler Helm仓库

执行命令：

```bash
helm repo add kepler https://sustainable-computing-io.github.io/kepler-helm-chart
```

您可以通过以下命令找到最新版本

```bash
helm search repo kepler
```

您可以执行以下命令来测试并检查生成的用于安装的配置文件。

```bash
helm install kepler kepler/kepler --namespace kepler --create-namespace --dry-run --devel
```

## 安装Kepler

执行命令：

```bash
helm install kepler kepler/kepler --namespace kepler --create-namespace
```

>您也许需要改变环境变量来适配您的实际情况[values.yaml](https://github.com/sustainable-computing-io/kepler-helm-chart/blob/main/chart/kepler/values.yaml).

并通过以下命令来使得改动生效

```bash
helm install kepler kepler/kepler --values values.yaml --namespace kepler --create-namespace
```

下表列出了配置参数的定义和默认值。

Parameter|Description| Default
---|---|---
global.namespace| Kubernetes namespace for kepler |kepler
image.repository|Repository for Kepler Image| quay.io/sustainable\_computing\_io/kepler
image.pullPolicy|Pull policy for Kepler|Always
image.tag|Image tag for Kepler Image |latest
serviceAccount.name|Service account name for Kepler|kepler-sa
service.type|Kepler service type|ClusterIP
service.port|Kepler service exposed port|9102

## 卸载 Kepler
您可以通过以下命令卸载
```bash
helm delete kepler --namespace kepler
```
