# 使用清单文件部署Kepler

## 开始之前

以下指令同时适用于`Kind`和`Kubeadm`集群。

### 前置条件

1. 已运行Kubernetes集群

    !!! 注意  
        如需搭建kind集群，请[参照此文档](./local-cluster.md#install-kind)

2. 已部署监控栈（即Prometheus与Grafana）。[部署步骤](#deploy-the-prometheus-operator)

    !!! 注意  
        默认Grafana部署可通过凭证`admin:admin`访问。  
        可通过以下命令在本地暴露Web界面：

    ```console
    kubectl -n monitoring port-forward svc/grafana 3000
    ```

满足前置条件后，请继续后续操作。

### 在本地kind集群部署Kepler

在`kind`上部署需使用特定标志本地构建，完整构建说明详见[下方章节](#build-manifests)。部署时需启用`PROMETHEUS_DEPLOY`标志：

```console
git clone --depth 1 git@github.com:sustainable-computing-io/kepler.git
cd ./kepler
make build-manifest OPTS="PROMETHEUS_DEPLOY"
kubectl apply -f _output/generated-manifest/deployment.yaml
```

### 在裸金属Kubeadm集群部署Kepler

在[Kubeadm][2]上部署需使用`BM_DEPLOY`和`PROMETHEUS_DEPLOY`标志：

```console
git clone --depth 1 git@github.com:sustainable-computing-io/kepler.git
cd ./kepler
make build-manifest OPTS="BM_DEPLOY PROMETHEUS_DEPLOY"
kubectl apply -f _output/generated-manifest/deployment.yaml
```

### 仪表板访问

上述部署将创建监听9102端口的Kepler服务。

若已部署仪表板，可通过[http://localhost:3000/](http://localhost:3000/)访问，使用`admin:admin`登录（可跳过修改密码提示）。

![Grafana仪表板](../fig/grafana_dashboard.png)

!!! 注意  
    端口转发命令：
    ```console
    kubectl port-forward --address localhost -n kepler service/kepler-exporter 9102:9102 &
    kubectl port-forward --address localhost -n monitoring service/prometheus-k8s 9090:9090 &
    kubectl port-forward --address localhost -n monitoring service/grafana 3000:3000 &
    ```

### 构建清单文件

首先fork并克隆[kepler](https://github.com/sustainable-computing-io/kepler)仓库。

如需使用Redfish BMC和IPMI，需在`kepler/manifests/k8s/config/exporter/redfish.csv`中添加各节点的凭证，格式如下：

```csv
kubelet节点名称1,redfish用户名1,redfish密码1,https://redfish地址1
kubelet节点名称2,redfish用户名2,redfish密码2,https://redfish地址2
```

可通过以下命令获取节点名称：
```console
kubectl get nodes
```

然后通过以下命令构建清单文件：

```console
make build-manifest OPTS="<部署选项>"
```

#### 部署选项说明

选项 | 描述 | 依赖项
---|---|---
BM_DEPLOY | 通过节点选择器部署裸金属环境 | -
OPENSHIFT_DEPLOY | 添加OpenShift专属属性并部署SecurityContextConstraints | -
PROMETHEUS_DEPLOY | 添加Prometheus相关资源 | 需预先部署Prometheus
HIGH_GRANULARITY | 设置Prometheus抓取间隔为3秒（默认30秒） | 需启用PROMETHEUS_DEPLOY
CLUSTER_PREREQ_DEPLOY | 部署OpenShift集群前置条件 | 需启用OPENSHIFT_DEPLOY
CI_DEPLOY | 为CI环境更新proc路径 | -
ESTIMATOR_SIDECAR_DEPLOY | 添加估算器边车容器 | -
MODEL_SERVER_DEPLOY | 部署模型服务器 | -
TRAINER_DEPLOY | 添加在线训练器边车 | 需启用MODEL_SERVER_DEPLOY
DEBUG_DEPLOY | 设置KEPLER_LOG_LEVEL调试级别 | -
QAT_DEPLOY | 启用QAT加速器支持 | 需安装Intel QAT
DCGM_DEPLOY | 启用hostNetwork访问DCGM服务 | 需安装NVIDIA DCGM

#### Redfish客户端选项

选项 | 默认值 | 描述
---|---|---
REDFISH_PROBE_INTERVAL_IN_SECONDS | 60 | Redfish功耗获取间隔(秒)
REDFISH_SKIP_SSL_VERIFY | true | 是否禁用TLS验证

#### 构建要求
- kubectl v1.21+
- make
- go

## 部署Prometheus Operator

若集群已安装Prometheus可跳过此步骤。

1. 克隆kube-prometheus项目：

    ```console
    git clone --depth 1 https://github.com/prometheus-operator/kube-prometheus; cd kube-prometheus;
    ```

2. （可选）自动添加Grafana仪表板：

    ```console
    $ KEPLER_EXPORTER_GRAFANA_DASHBOARD_JSON=`curl -fsSL https://raw.githubusercontent.com/sustainable-computing-io/kepler/main/grafana-dashboards/Kepler-Exporter.json | sed '1 ! s/^/         /'`
    $ mkdir -p grafana-dashboards
    $ cat - > ./grafana-dashboards/kepler-exporter-configmap.yaml << EOF
    apiVersion: v1
    data:
        kepler-exporter.json: |-
            $KEPLER_EXPORTER_GRAFANA_DASHBOARD_JSON
    kind: ConfigMap
    metadata:
        labels:
            app.kubernetes.io/component: grafana
            app.kubernetes.io/name: grafana
            app.kubernetes.io/part-of: kube-prometheus
            app.kubernetes.io/version: 9.5.3
        name: grafana-dashboard-kepler-exporter
        namespace: monitoring
    EOF
    ```

    使用yq工具注入配置：

    ```console
    yq -i e '.items += [load("./grafana-dashboards/kepler-exporter-configmap.yaml")]' ./manifests/grafana-dashboardDefinitions.yaml
    yq -i e '.spec.template.spec.containers.0.volumeMounts += [ {"mountPath": "/grafana-dashboard-definitions/0/kepler-exporter", "name": "grafana-dashboard-kepler-exporter", "readOnly": false} ]' ./manifests/grafana-deployment.yaml
    yq -i e '.spec.template.spec.volumes += [ {"configMap": {"name": "grafana-dashboard-kepler-exporter"}, "name": "grafana-dashboard-kepler-exporter"} ]' ./manifests/grafana-deployment.yaml
    ```

3. 应用清单文件：

    ```console
    kubectl apply --server-side -f manifests/setup
    until kubectl get servicemonitors --all-namespaces ; do date; sleep 1; echo ""; done
    kubectl apply -f manifests/
    ```

    !!! 注意  
        所有Pod和服务进入`running`状态可能需要短暂等待（Kind集群中）。

[1]:https://raw.githubusercontent.com/sustainable-computing-io/kepler/main/grafana-dashboards/Kepler-Exporter.json
[2]:https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/

（译文严格遵循技术文档翻译规范，专业术语准确统一，被动语态转换为中文主动表述，长句合理切分，保留所有代码块与格式标记）