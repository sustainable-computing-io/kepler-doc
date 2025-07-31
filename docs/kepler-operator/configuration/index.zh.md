# PowerMonitor 配置指南

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

本指南涵盖了 PowerMonitor 自定义资源定义（CRD）的全面配置选项。使用这些设置为不同环境、安全要求和监控需求自定义您的 Kepler 部署。

## 基本配置

### 指标级别

控制 Kepler 导出的指标类型。根据您的监控要求和性能考虑进行选择：

```yaml
spec:
  kepler:
    config:
      metricLevels:
      - node      # 节点级功耗（推荐）
      - pod       # Pod 级功耗（推荐）
      - vm        # 虚拟机功耗
      - process   # 进程级功耗（高开销）
      - container # 容器级功耗（高开销）
```

**推荐：**

- **生产环境**：使用 `node` 和 `pod` 获得平衡的监控
- **开发环境**：添加 `container` 进行详细分析
- **最小开销**：仅使用 `node`

### 时序配置

配置 Kepler 采样和报告指标的频率：

```yaml
spec:
  kepler:
    config:
      sampleRate: 5s      # 采样指标的频率
      staleness: 500ms    # 值被认为过时的时间
```

**性能调优：**

- **降低 CPU 使用率**：将 `sampleRate` 增至 `10s` 或 `15s`
- **更高精度**：将 `sampleRate` 减至 `3s`（推荐最小值）
- **网络优化**：根据网络延迟调整 `staleness`

### 日志配置

设置用于故障排除和监控的日志级别：

```yaml
spec:
  kepler:
    config:
      logLevel: info  # 选项：debug, info, warn, error
```

**日志级别：**

- **`debug`**：用于故障排除的详细日志（不适用于生产环境）
- **`info`**：标准操作日志（推荐）
- **`warn`**：仅警告和错误
- **`error`**：仅错误消息

## 资源管理

### 已终止工作负载跟踪

控制 Kepler 如何处理已终止 Pod 和容器的指标：

```yaml
spec:
  kepler:
    config:
      maxTerminated: 500  # 按功耗跟踪前 500 个已终止工作负载
```

**选项：**

- **`500`**（默认）：跟踪前 500 个已终止工作负载
- **`0`**：禁用已终止工作负载跟踪（节省内存）
- **`-1`**：跟踪无限制的已终止工作负载（请谨慎使用）

### 额外 ConfigMap

使用外部 ConfigMap 进行高级配置：

```yaml
spec:
  kepler:
    config:
      additionalConfigMaps:
      - name: custom-model-config
      - name: advanced-power-settings
```

这允许您：

- 覆盖功率模型
- 自定义 CPU 频率映射
- 配置平台特定设置

## 安全配置

### RBAC 模式

配置安全和服务账户权限：

```yaml
spec:
  kepler:
    deployment:
      security:
        mode: rbac              # 选项：none, rbac
        allowedSANames:
        - "monitoring-sa"
        - "custom-service-account"
```

**安全模式：**

- **`none`**：无额外安全限制（开发环境默认）
- **`rbac`**：启用基于角色的访问控制（生产环境推荐）

### 服务账户配置

使用 RBAC 模式时，指定允许的服务账户：

```yaml
spec:
  kepler:
    deployment:
      security:
        mode: rbac
        allowedSANames:
        - "prometheus-service-account"
        - "grafana-service-account"
```

## 节点选择和调度

### 节点选择器

控制哪些节点运行 Kepler Pod：

```yaml
spec:
  kepler:
    deployment:
      nodeSelector:
        kubernetes.io/os: linux
        node-type: worker
        monitoring: enabled
```

常见选择器：

- **操作系统选择**：`kubernetes.io/os: linux`
- **节点角色**：`node-role.kubernetes.io/worker: ""`
- **自定义标签**：`monitoring: enabled`

### 容忍度

允许 Kepler 在具有特定污点的节点上运行：

```yaml
spec:
  kepler:
    deployment:
      tolerations:
      - key: node-role.kubernetes.io/master
        operator: Exists
        effect: NoSchedule
      - key: dedicated
        operator: Equal
        value: monitoring
        effect: NoSchedule
```

**常见容忍度：**

- **主节点**：允许在控制平面节点上监控
- **专用节点**：在专用于监控的节点上运行
- **特殊硬件**：具有特定硬件要求的节点

## 完整配置示例

### 开发环境

```yaml
apiVersion: kepler.system.sustainable.computing.io/v1alpha1
kind: PowerMonitor
metadata:
  name: power-monitor-dev
spec:
  kepler:
    config:
      logLevel: debug
      metricLevels:
      - node
      - pod
      - container
      sampleRate: 3s
      staleness: 200ms
      maxTerminated: 100
    deployment:
      security:
        mode: none
```

### 生产环境

```yaml
apiVersion: kepler.system.sustainable.computing.io/v1alpha1
kind: PowerMonitor
metadata:
  name: power-monitor-prod
spec:
  kepler:
    config:
      logLevel: warn
      metricLevels:
      - node
      - pod
      sampleRate: 10s
      staleness: 1s
      maxTerminated: 1000
    deployment:
      security:
        mode: rbac
        allowedSANames:
        - "prometheus-operator-prometheus"
      nodeSelector:
        kubernetes.io/os: linux
        node-role.kubernetes.io/worker: ""
      tolerations:
      - key: dedicated
        operator: Equal
        value: monitoring
        effect: NoSchedule
```

### 高性能监控

```yaml
apiVersion: kepler.system.sustainable.computing.io/v1alpha1
kind: PowerMonitor
metadata:
  name: power-monitor-hpc
spec:
  kepler:
    config:
      logLevel: info
      metricLevels:
      - node
      - pod
      - vm
      - process
      sampleRate: 1s
      staleness: 100ms
      maxTerminated: -1  # 跟踪所有已终止工作负载
      additionalConfigMaps:
      - name: hpc-power-models
    deployment:
      security:
        mode: rbac
      nodeSelector:
        node-type: compute-intensive
      tolerations:
      - key: high-performance
        operator: Exists
        effect: NoSchedule
```

## 配置验证

### 检查配置

验证您的 PowerMonitor 配置：

```bash
# 检查 PowerMonitor 状态
oc get powermonitor power-monitor -o yaml

# 验证条件
oc describe powermonitor power-monitor

# 检查生成的资源
oc get all -n power-monitor
```

### 常见配置问题

**问题**：Pod 未在预期节点上调度

```bash
# 检查节点标签
oc get nodes --show-labels

# 更新 nodeSelector
oc patch powermonitor power-monitor --type='merge' -p='
{
  "spec": {
    "kepler": {
      "deployment": {
        "nodeSelector": {
          "kubernetes.io/os": "linux"
        }
      }
    }
  }
}'
```

**问题**：高资源使用率

```bash
# 减少指标级别并增加采样率
oc patch powermonitor power-monitor --type='merge' -p='
{
  "spec": {
    "kepler": {
      "config": {
        "metricLevels": ["node", "pod"],
        "sampleRate": "10s"
      }
    }
  }
}'
```

## 高级主题

有关更高级的配置场景，请参阅：

- **[监控和故障排除](monitoring-troubleshooting.zh.md)** - 高级监控设置
- **[迁移指南](../migration/index.zh.md)** - 从旧配置迁移
