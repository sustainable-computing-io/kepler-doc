```markdown
# 在Kind上部署Kepler Operator

## 前置要求

开始前请确保已安装：
- `docker` 并以非root用户默认运行
- `kubectl` 命令行工具
- `kind` 集群工具
- 克隆 `kepler-operator` [代码库](https://github.com/sustainable-computing-io/kepler-operator)
- 以 `kubeadmin` 或具有 `cluster-admin` 权限的用户登录

!!! 注意  
    控制器会自动使用当前kubeconfig中的上下文（即`kubectl cluster-info`显示的集群）。

## 本地运行kind集群

```sh
cd kepler-operator
make cluster-up
```

## 运行kepler-operator

- 使用quay.io镜像部署：

    ```sh
    make deploy OPERATOR_IMG=quay.io/sustainable_computing_io/kepler-operator:[版本号]
    kubectl apply -k config/samples/
    ```

- 如需从头构建自定义镜像：

    ```sh
    make fresh
    ```

    此命令将创建kind集群，并将operator和bundle镜像推送到本地仓库。

## 配置Grafana仪表盘

在运行`make cluster-up`时添加`GRAFANA_ENABLE=true`和`PROMETHEUS_ENABLE=true`参数，会在`monitoring`命名空间部署`kube-prometheus`监控栈。  
通过端口转发访问本地Grafana控制台：

```sh
kubectl port-forward svc/grafana 3000:3000 -n monitoring
```

!!! 提示  
    Grafana控制台可通过 [http://localhost:3000](http://localhost:3000) 访问

### 服务监控

需配置ServiceMonitor才能使`kube-prometheus`抓取`kepler-exporter`的服务端点。

!!! 注意  
    默认情况下`kube-prometheus`仅监控`monitoring`命名空间的服务。  
    若Kepler运行在其他命名空间，[需按此配置Prometheus全局抓取](#scrape-all-namespaces)。

```cmd
kubectl apply -n monitoring -f - << EOF
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  labels:
    app.kubernetes.io/component: exporter
    app.kubernetes.io/name: kepler-exporter
    sustainable-computing.io/app: kepler
  name: monitor-kepler-exporter
spec:
  endpoints:
  - interval: 3s
    port: http
    relabelings:
    - action: replace
      regex: (.*)
      replacement: $1
      sourceLabels:
      - __meta_kubernetes_pod_node_name
      targetLabel: instance
    scheme: http
  jobLabel: app.kubernetes.io/name
  namespaceSelector:
    matchNames:
    any: true
  selector:
    matchLabels:
      app.kubernetes.io/component: exporter
      app.kubernetes.io/name: kepler-exporter
EOF
```

### Grafana仪表盘

配置步骤：
1. 使用`admin:admin`登录 [localhost:3000](http:localhost:3000)
2. 导入Operator代码库中的[默认仪表盘](https://raw.githubusercontent.com/sustainable-computing-io/kepler-operator/v1alpha1/hack/dashboard/assets/kepler/dashboard.json)

    ![kind-grafana](../fig/ocp_installation/kind_grafana.png)

## 卸载Operator

删除集群中的CRDs、角色、角色绑定等资源：

```sh
make undeploy
```

## 故障排查

### 全局命名空间抓取

默认`kube-prometheus`不监控`monitoring`外的命名空间，这由RBAC控制。需确保集群角色`prometheus-k8s`包含以下策略：

```sh
kubectl describe clusterrole prometheus-k8s
# 输出内容显示需包含对endpoints/pods/services等资源的get/list/watch权限
```

- 集群创建后，参考kube-prometheus官方文档[自定义配置](https://github.com/prometheus-operator/kube-prometheus/blob/main/docs/customizing.md)
- 应用[此jsonnet配置](https://github.com/prometheus-operator/kube-prometheus/blob/main/docs/customizations/monitoring-all-namespaces.md)实现全局监控
``` 

（注：保留了所有技术术语的英文原称如Prometheus/Grafana/CRDs等，Markdown格式与原始文档完全一致，中文表述符合技术文档规范）