```markdown
# Kepler 安装指南

本指南介绍多种安装和运行Kepler（基于Kubernetes的高效能耗监控导出器）的方法，用于监测能源消耗指标。

## 先决条件

- **本地安装**：Go 1.21+ 版本及硬件传感器访问所需的sudo权限
- **Kubernetes环境**：已配置kubectl的Kubernetes集群（v1.20+）
- **Helm安装**：已安装Helm 3.0+

## 安装方法

### 1. Helm Chart安装（Kubernetes推荐方案）

#### Helm先决条件

- Helm 3.0+
- 已配置kubectl的Kubernetes集群

#### 从Release安装（推荐）

```bash
# 从GitHub release安装（将VERSION替换为目标版本，如v0.10.2）
helm install kepler \
  https://github.com/sustainable-computing-io/kepler/releases/download/VERSION/kepler-helm-VERSION.tgz \
  --namespace kepler \
  --create-namespace

# 指定版本示例：
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

# 使用Helm安装
helm install kepler manifests/helm/kepler/ \
  --namespace kepler \
  --create-namespace \
  --set namespace.create=false
```

#### 自定义安装

创建`values.yaml`文件进行配置：

```yaml
# values.yaml示例
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

# 启用Prometheus的ServiceMonitor
serviceMonitor:
  enabled: true
  interval: 30s
```

使用自定义配置安装：

```bash
helm install kepler manifests/helm/kepler/ \
  --namespace kepler \
  --create-namespace \
  --set namespace.create=false \
  --values values.yaml
```

#### Helm管理命令

```bash
# 检查安装状态
helm status kepler -n kepler

# 列出release
helm list -n kepler

# 升级release
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

# 构建Kepler
make build

# 运行（需sudo权限访问硬件）
sudo ./bin/kepler --config hack/config.yaml
```

#### 配置

可通过YAML文件或CLI参数配置，默认配置位于`hack/config.yaml`：

```bash
# 使用自定义配置运行
sudo ./bin/kepler --config /path/to/your/config.yaml

# 使用CLI参数运行
sudo ./bin/kepler --log.level=debug --exporter.stdout
```

**访问端点**：

- 指标数据：<http://localhost:28282/metrics>

### 3. Docker Compose（开发推荐）

提供包含Kepler、Prometheus和Grafana的完整监控栈：

```bash
cd compose/dev

# 启动完整监控栈
docker-compose up -d

# 查看日志
docker-compose logs -f kepler

# 停止服务
docker-compose down
```

**访问端点**：

- Kepler指标：<http://localhost:28283/metrics>
- Prometheus：<http://localhost:29090>
- Grafana：<http://localhost:23000> (账号/密码：admin/admin)

### 4. Kubernetes Kustomize部署

#### 快速Kind集群部署

```bash
# 创建带监控栈的本地集群
make cluster-up

# 部署Kepler
make deploy

# 清理环境
make cluster-down
```

#### 手动Kubernetes部署

```bash
# 使用kustomize部署
kubectl kustomize manifests/k8s | \
  sed -e "s|<KEPLER_IMAGE>|quay.io/sustainable_computing_io/kepler:latest|g" | \
  kubectl apply --server-side --force-conflicts -f -

# 检查部署状态
kubectl get pods -n kepler

# 端口转发访问指标
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
# 检查Pod状态
kubectl get pods -n kepler

# 检查DaemonSet
kubectl get daemonset -n kepler

# 检查服务
kubectl get svc -n kepler

# 查看日志
kubectl logs -n kepler -l app.kubernetes.io/name=kepler
```

### 访问指标数据

```bash
# 端口转发本地访问
kubectl port-forward -n kepler svc/kepler 28282:28282

# 测试指标端点
curl http://localhost:28282/metrics
```

### 验证指标收集

检查关键指标如：

- `kepler_node_cpu_watts`
- `kepler_container_cpu_watts`
- `kepler_process_cpu_watts`

## 配置选项

### Helm Chart参数

`values.yaml`中的关键配置：

```yaml
# 镜像配置
image:
  repository: quay.io/sustainable_computing_io/kepler
  tag: "latest"
  pullPolicy: IfNotPresent

# DaemonSet配置
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

# 监控配置
serviceMonitor:
  enabled: true
  interval: 30s
  scrapeTimeout: 10s
```

### 环境特定设置

- **开发环境**：当RAPL不可用时启用模拟CPU计量器
- **生产环境**：确保节点支持Intel RAPL
- **云环境**：可能需要不同的权限配置

## 故障排查

### 常见问题

1. **权限拒绝**：确保启用privileged安全上下文
2. **无指标数据**：检查节点是否支持Intel RAPL传感器
3. **Pod崩溃**：检查硬件访问相关的日志
4. **ServiceMonitor未找到**：确保已安装Prometheus Operator

### 调试命令

```bash
# 查看Pod日志
kubectl logs -n kepler -l app.kubernetes.io/name=kepler

# 查看Pod事件
kubectl describe pod -n kepler -l app.kubernetes.io/name=kepler

# 检查节点硬件
kubectl exec -n kepler -it <pod-name> -- ls /sys/class/powercap/intel-rapl

# 开发环境使用模拟计量器
helm upgrade kepler manifests/helm/kepler/ -n kepler \
  --set env.KEPLER_FAKE_CPU_METER=true
```

### 获取帮助

- **文档**：<https://sustainable-computing.io/kepler/>
- **问题反馈**：<https://github.com/sustainable-computing-io/kepler/issues>
- **讨论区**：<https://github.com/sustainable-computing-io/kepler/discussions>
- **Slack**：[CNCF Slack的#kepler频道](https://cloud-native.slack.com/archives/C06HYDN4A01)

## 后续步骤

安装成功后建议：

1. **配置Prometheus**：设置Kepler指标抓取
2. **安装Grafana**：使用预构建仪表板可视化数据
3. **设置告警**：配置能耗告警规则
4. **探索指标**：了解可用能耗指标
5. **优化工作负载**：利用洞察提升能效
``` 

注：所有代码块、URL链接和专有名词（如Kepler/RAPL等）均保留原始英文格式，符合技术文档惯例。