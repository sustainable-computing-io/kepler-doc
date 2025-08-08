# Kepler 安装指南

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

本指南涵盖了安装和运行 Kepler（基于 Kubernetes 的高效功率级别导出器）以监控能耗指标的不同方法。

## 先决条件

- **本地安装**：Go 1.21+ 和 sudo 权限以访问硬件传感器
- **Kubernetes**：Kubernetes 集群（v1.20+）且已配置 kubectl
- **Helm**：已安装 Helm 3.0+

## 安装方法

### 1. Helm Chart 安装（推荐用于 Kubernetes）

#### Helm 先决条件

- Helm 3.0+
- 已配置 kubectl 的 Kubernetes 集群

#### 从发布版安装（推荐）

```bash
# 从 GitHub 发布版安装（将 VERSION 替换为所需版本，例如 v0.10.2）
helm install kepler \
  https://github.com/sustainable-computing-io/kepler/releases/download/VERSION/kepler-helm-VERSION.tgz \
  --namespace kepler \
  --create-namespace

# 指定版本的示例：
# helm install kepler \
#   https://github.com/sustainable-computing-io/kepler/releases/download/v0.10.2/kepler-helm-0.10.2.tgz \
#   --namespace kepler \
#   --create-namespace
```

#### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/sustainable-computing-io/kepler.git
cd kepler

# 使用 Helm 安装 Kepler
helm install kepler manifests/helm/kepler/ \
  --namespace kepler \
  --create-namespace \
  --set namespace.create=false
```

#### 自定义安装

创建 `values.yaml` 文件来自定义安装：

```yaml
# values.yaml
image:
  repository: quay.io/sustainable_computing_io/kepler
  tag: "v0.10.0"
  pullPolicy: IfNotPresent

resources:
  limits:
    cpu: 100m
    memory: 400Mi
  requests:
    cpu: 100m
    memory: 200Mi

tolerations:
  - operator: Exists

nodeSelector:
  kubernetes.io/os: linux

# 为 Prometheus 启用 ServiceMonitor
serviceMonitor:
  enabled: true
  interval: 30s
```

使用自定义值安装：

```bash
helm install kepler manifests/helm/kepler/ \
  --namespace kepler \
  --create-namespace \
  --set namespace.create=false \
  --values values.yaml
```

#### Helm 管理命令

```bash
# 检查安装状态
helm status kepler -n kepler

# 列出发布版
helm list -n kepler

# 升级发布版
helm upgrade kepler manifests/helm/kepler/ -n kepler

# 卸载
helm uninstall kepler -n kepler
```

### 2. 本地安装

#### 从源码构建

```bash
# 克隆仓库
git clone https://github.com/sustainable-computing-io/kepler.git
cd kepler

# 构建 Kepler
make build

# 运行 Kepler（需要 sudo 权限访问硬件）
sudo ./bin/kepler --config hack/config.yaml
```

#### 配置

Kepler 可以使用 YAML 文件或 CLI 标志进行配置。默认配置在 `hack/config.yaml` 中：

```bash
# 使用自定义配置运行
sudo ./bin/kepler --config /path/to/your/config.yaml

# 使用 CLI 标志运行
sudo ./bin/kepler --log.level=debug --exporter.stdout
```

**访问端点：**

- 指标：<http://localhost:28282/metrics>

### 3. Docker Compose（推荐用于开发）

Docker Compose 设置提供了包含 Kepler、Prometheus 和 Grafana 的完整监控堆栈：

```bash
cd compose/dev

# 启动完整堆栈
docker compose up -d

# 查看日志
docker compose logs -f kepler

# 停止堆栈
docker compose down
```

**访问端点：**

- Kepler 指标：<http://localhost:28283/metrics>
- Prometheus：<http://localhost:29090>
- Grafana：<http://localhost:23000>（admin/admin）

### 4. 使用 Kustomize 的 Kubernetes

#### 使用 Kind 快速设置

```bash
# 创建带监控堆栈的本地集群
make cluster-up

# 部署 Kepler
make deploy

# 清理
make cluster-down
```

#### 手动 Kubernetes 部署

```bash
# 使用 kustomize 部署
kubectl kustomize manifests/k8s | \
  sed -e "s|<KEPLER_IMAGE>|quay.io/sustainable_computing_io/kepler:latest|g" | \
  kubectl apply --server-side --force-conflicts -f -

# 检查部署状态
kubectl get pods -n kepler

# 访问指标（端口转发）
kubectl port-forward -n kepler svc/kepler 28282:28282
```

#### 自定义镜像部署

```bash
# 构建并推送自定义镜像
make image push IMG_BASE=your-registry.com/yourorg VERSION=v1.0.0

# 使用自定义镜像部署
make deploy IMG_BASE=your-registry.com/yourorg VERSION=v1.0.0
```

## 验证

### 检查部署状态

```bash
# 检查 Pod
kubectl get pods -n kepler

# 检查 DaemonSet
kubectl get daemonset -n kepler

# 检查服务
kubectl get svc -n kepler

# 查看日志
kubectl logs -n kepler -l app.kubernetes.io/name=kepler
```

### 访问指标

```bash
# 端口转发以本地访问指标
kubectl port-forward -n kepler svc/kepler 28282:28282

# 测试指标端点
curl http://localhost:28282/metrics
```

### 验证指标收集

查找关键指标，如：

- `kepler_node_cpu_watts`
- `kepler_container_cpu_watts`
- `kepler_process_cpu_watts`

## 配置选项

### Helm Chart 值

`values.yaml` 中的关键配置选项：

```yaml
# 镜像配置
image:
  repository: quay.io/sustainable_computing_io/kepler
  tag: "latest"
  pullPolicy: IfNotPresent

# DaemonSet 配置
daemonset:
  hostPID: true
  securityContext:
    privileged: true

# 资源限制
resources:
  limits:
    cpu: 100m
    memory: 400Mi
  requests:
    cpu: 100m
    memory: 200Mi

# 节点调度
tolerations:
  - operator: Exists

nodeSelector:
  kubernetes.io/os: linux

# 监控
serviceMonitor:
  enabled: true
  interval: 30s
  scrapeTimeout: 10s
```

### 环境特定设置

- **开发**：在 RAPL 不可用时使用假 CPU 计量器
- **生产**：确保节点支持 Intel RAPL
- **云端**：可能需要不同的权限配置

## 故障排除

### 常见问题

1. **权限被拒绝**：确保启用了特权安全上下文
2. **无指标**：检查节点是否支持 Intel RAPL 传感器
3. **Pod 崩溃**：查看日志了解硬件访问问题
4. **找不到 ServiceMonitor**：确保已安装 Prometheus Operator

### 调试命令

```bash
# 检查 Pod 日志
kubectl logs -n kepler -l app.kubernetes.io/name=kepler

# 描述 Pod 以查看事件
kubectl describe pod -n kepler -l app.kubernetes.io/name=kepler

# 检查节点硬件
kubectl exec -n kepler -it <pod-name> -- ls /sys/class/powercap/intel-rapl

# 使用假计量器进行测试（开发）
helm upgrade kepler manifests/helm/kepler/ -n kepler \
  --set env.KEPLER_FAKE_CPU_METER=true
```

### 获取帮助

- **文档**：<https://sustainable-computing.io/kepler/>
- **问题**：<https://github.com/sustainable-computing-io/kepler/issues>
- **讨论**：<https://github.com/sustainable-computing-io/kepler/discussions>
- **Slack**：[CNCF Slack 中的 #kepler 频道](https://cloud-native.slack.com/archives/C06HYDN4A01)

## 后续步骤

成功安装后：

1. **设置 Prometheus**：配置 Kepler 指标抓取
2. **安装 Grafana**：使用预构建的仪表板进行可视化
3. **配置告警**：设置能耗告警
4. **探索指标**：了解可用的能耗指标
5. **优化工作负载**：使用洞察来提高能效
