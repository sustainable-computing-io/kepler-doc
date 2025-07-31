# 迁移指南：从 Kepler CRD 到 PowerMonitor

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

本指南帮助您从已弃用的 Kepler CRD 迁移到现代的 PowerMonitor CRD。PowerMonitor 提供增强的配置选项、改进的资源管理和更好的 OpenShift 集成。

## 迁移概述

### 为什么要迁移？

!!! warning "弃用通知"
    Kepler CRD 已被弃用，将在未来版本中删除。迁移到 PowerMonitor 以确保持续支持并访问新功能。

**PowerMonitor 的优势：**

- 增强的安全配置
- 改进的资源管理
- 更好的 OpenShift 集成
- 更精细的指标控制
- 积极的开发和支持

### 迁移影响

**零宕机迁移：** 迁移过程允许您在过渡期间同时运行两个 CRD，确保持续监控。

**配置差异：** 一些配置选项已更改或重新组织。本指南提供了新旧配置之间的映射。

## 迁移前评估

### 步骤 1：清点当前部署

记录现有的 Kepler CRD 配置：

```bash
# 列出现有的 Kepler 资源
oc get kepler --all-namespaces

# 导出当前配置
oc get kepler kepler -o yaml > kepler-backup.yaml

# 保存当前 DaemonSet 配置以供参考
oc get daemonset -n kepler -o yaml > kepler-daemonset-backup.yaml
```

### 步骤 2：审视配置映射

常见配置更改：

| Kepler CRD（旧） | PowerMonitor CRD（新） |
|-------------------|------------------------|
| `spec.exporter.deployment.port` | 自动管理 |
| `spec.exporter.config.logLevel` | `spec.kepler.config.logLevel` |
| `spec.nodeSelector` | `spec.kepler.deployment.nodeSelector` |
| `spec.tolerations` | `spec.kepler.deployment.tolerations` |

## 迁移流程

### 步骤 1：创建等效的 PowerMonitor

#### 示例迁移：基本配置

**旧 Kepler CRD：**

```yaml
apiVersion: kepler.system.sustainable.computing.io/v1alpha1
kind: Kepler
metadata:
  name: kepler
spec:
  exporter:
    deployment:
      port: 9102
    config:
      logLevel: info
  nodeSelector:
    kubernetes.io/os: linux
```

**新 PowerMonitor CRD：**

```yaml
apiVersion: kepler.system.sustainable.computing.io/v1alpha1
kind: PowerMonitor
metadata:
  name: power-monitor
  labels:
    app.kubernetes.io/name: powermonitor
    app.kubernetes.io/instance: powermonitor
    app.kubernetes.io/part-of: kepler-operator
spec:
  kepler:
    config:
      logLevel: info
      metricLevels:
      - node
      - pod
      - vm
      sampleRate: 5s
    deployment:
      nodeSelector:
        kubernetes.io/os: linux
      security:
        mode: none
```

#### 示例迁移：高级配置

**旧 Kepler CRD：**

```yaml
apiVersion: kepler.system.sustainable.computing.io/v1alpha1
kind: Kepler
metadata:
  name: kepler
spec:
  exporter:
    config:
      logLevel: warn
  nodeSelector:
    node-role.kubernetes.io/worker: ""
  tolerations:
  - key: node-role.kubernetes.io/master
    operator: Exists
    effect: NoSchedule
```

**新 PowerMonitor CRD：**

```yaml
apiVersion: kepler.system.sustainable.computing.io/v1alpha1
kind: PowerMonitor
metadata:
  name: power-monitor
spec:
  kepler:
    config:
      logLevel: warn
      metricLevels: [node, pod]
      sampleRate: 10s
      maxTerminated: 500
    deployment:
      nodeSelector:
        node-role.kubernetes.io/worker: ""
      tolerations:
      - key: node-role.kubernetes.io/master
        operator: Exists
        effect: NoSchedule
      security:
        mode: rbac
```

### 步骤 2：在现有 Kepler 旁部署 PowerMonitor

在保持旧 Kepler CRD 运行的同时部署 PowerMonitor：

```bash
# 创建 PowerMonitor 配置
cat > power-monitor.yaml << EOF
apiVersion: kepler.system.sustainable.computing.io/v1alpha1
kind: PowerMonitor
metadata:
  name: power-monitor
spec:
  kepler:
    config:
      logLevel: info
      metricLevels: [node, pod, vm]
      sampleRate: 5s
    deployment:
      security:
        mode: none
EOF

# 应用 PowerMonitor
oc apply -f power-monitor.yaml
```

### 步骤 3：验证 PowerMonitor 功能

确保 PowerMonitor 正常工作：

```bash
# 检查 PowerMonitor 状态
oc get powermonitor power-monitor -o wide

# 验证 DaemonSet 创建
oc get daemonset -n power-monitor

# 检查 pod 是否正在运行
oc get pods -n power-monitor

# 测试指标端点
oc port-forward -n power-monitor svc/kepler-exporter 9103:9102 &
curl http://localhost:9103/metrics | head -10
```

### 步骤 4：更新监控配置

如果您有现有的监控设置，请更新它以使用新的 PowerMonitor：

#### Prometheus ServiceMonitor

为新命名空间更新或创建 ServiceMonitor：

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: kepler-exporter
  namespace: power-monitor
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: kepler-exporter
  endpoints:
  - port: http
    path: /metrics
```

#### Grafana 仪表板

更新 Grafana 查询以使用新服务：

```promql
# 从以下查询更新：
{__name__=~"kepler_.*", job="kepler"}

# 到：
{__name__=~"kepler_.*", job="kepler-exporter", namespace="power-monitor"}
```

### 步骤 5：删除旧 Kepler CRD

在验证 PowerMonitor 正常工作后：

```bash
# 删除旧 Kepler 资源
oc delete kepler kepler

# 清理旧命名空间（如果不同）
oc delete namespace kepler

# 验证清理
oc get kepler --all-namespaces
```

## 配置迁移参考

### 完整映射表

| 旧配置 | 新配置 | 注释 |
|------------------|-------------------|-------|
| `spec.exporter.config.logLevel` | `spec.kepler.config.logLevel` | 相同值 |
| `spec.exporter.deployment.port` | 自动管理 | 默认端口 9102 |
| `spec.nodeSelector` | `spec.kepler.deployment.nodeSelector` | 相同格式 |
| `spec.tolerations` | `spec.kepler.deployment.tolerations` | 相同格式 |
| N/A | `spec.kepler.config.metricLevels` | 新：控制指标粒度 |
| N/A | `spec.kepler.config.sampleRate` | 新：控制采样频率 |
| N/A | `spec.kepler.deployment.security` | 新：RBAC 和安全选项 |
| N/A | `spec.kepler.config.maxTerminated` | 新：控制已终止工作负载跟踪 |

### 迁移脚本

使用此脚本自动化迁移：

```bash
#!/bin/bash
# migrate-kepler-to-powermonitor.sh

set -e

KEPLER_NAME="${1:-kepler}"
POWERMONITOR_NAME="${2:-power-monitor}"

echo "将 Kepler CRD '${KEPLER_NAME}' 迁移到 PowerMonitor '${POWERMONITOR_NAME}'"

# 导出当前 Kepler 配置
echo "导出当前 Kepler 配置..."
oc get kepler ${KEPLER_NAME} -o yaml > kepler-backup-$(date +%Y%m%d-%H%M%S).yaml

# 提取配置值
LOG_LEVEL=$(oc get kepler ${KEPLER_NAME} -o jsonpath='{.spec.exporter.config.logLevel}' 2>/dev/null || echo "info")
NODE_SELECTOR=$(oc get kepler ${KEPLER_NAME} -o jsonpath='{.spec.nodeSelector}' 2>/dev/null || echo "{}")
TOLERATIONS=$(oc get kepler ${KEPLER_NAME} -o jsonpath='{.spec.tolerations}' 2>/dev/null || echo "[]")

echo "使用等效配置创建 PowerMonitor..."

# 创建 PowerMonitor
cat > powermonitor-migration.yaml << EOF
apiVersion: kepler.system.sustainable.computing.io/v1alpha1
kind: PowerMonitor
metadata:
  name: ${POWERMONITOR_NAME}
  labels:
    app.kubernetes.io/name: powermonitor
    app.kubernetes.io/instance: powermonitor
    app.kubernetes.io/part-of: kepler-operator
    migrated-from: kepler-crd
spec:
  kepler:
    config:
      logLevel: ${LOG_LEVEL}
      metricLevels: [node, pod, vm]
      sampleRate: 5s
      maxTerminated: 500
    deployment:
      security:
        mode: none
EOF

# 如果存在 nodeSelector 则添加
if [ "${NODE_SELECTOR}" != "{}" ]; then
  echo "      nodeSelector:" >> powermonitor-migration.yaml
  echo "${NODE_SELECTOR}" | sed 's/^/        /' >> powermonitor-migration.yaml
fi

# 如果存在 tolerations 则添加
if [ "${TOLERATIONS}" != "[]" ]; then
  echo "      tolerations:" >> powermonitor-migration.yaml
  echo "${TOLERATIONS}" | sed 's/^/      /' >> powermonitor-migration.yaml
fi

# 应用 PowerMonitor
oc apply -f powermonitor-migration.yaml

echo "等待 PowerMonitor 准备就绪..."
sleep 10

# 验证 PowerMonitor
if oc get powermonitor ${POWERMONITOR_NAME} &>/dev/null; then
  echo "PowerMonitor 创建成功！"
  echo "验证 DaemonSet..."

  # 等待 DaemonSet
  timeout 60s bash -c "while ! oc get daemonset -n power-monitor | grep -q kepler; do sleep 2; done"

  echo "迁移完成！"
  echo "运行以下命令进行验证："
  echo "  oc get powermonitor ${POWERMONITOR_NAME}"
  echo "  oc get pods -n power-monitor"
  echo ""
  echo "验证后，删除旧的 Kepler CRD："
  echo "  oc delete kepler ${KEPLER_NAME}"
else
  echo "迁移失败。检查 PowerMonitor 配置。"
  exit 1
fi
```

使用方法：

```bash
chmod +x migrate-kepler-to-powermonitor.sh
./migrate-kepler-to-powermonitor.sh [kepler-name] [powermonitor-name]
```

## 回滚程序

如果您需要回滚到 Kepler CRD：

### 步骤 1：重新创建 Kepler CRD

```bash
# 应用您备份的 Kepler 配置
oc apply -f kepler-backup.yaml
```

### 步骤 2：删除 PowerMonitor

```bash
# 删除 PowerMonitor
oc delete powermonitor power-monitor

# 清理命名空间
oc delete namespace power-monitor
```

### 步骤 3：验证 Kepler CRD

```bash
# 检查 Kepler 状态
oc get kepler kepler
oc get pods -n kepler
```

## 迁移后任务

### 更新文档

- 更新内部文档以引用 PowerMonitor
- 更新自动化脚本和 CI/CD 流水线
- 培训团队成员使用新配置选项

### 监控集成

- 为新命名空间和服务名称更新告警规则
- 验证监控系统中的指标收集
- 使用新服务发现更新仪表板

### 清理

- 成功迁移后删除备份文件
- 清理旧的监控配置
- 更新基础设施即代码（IaC）模板

## 获取帮助

如果在迁移过程中遇到问题：

1. **检查日志**：使用[故障排除指南](../configuration/monitoring-troubleshooting.zh.md)中的诊断命令
2. **社区支持**：查看[支持](../../project/support.zh.md)了解社区渠道
3. **报告问题**：在 [Kepler Operator 仓库](https://github.com/sustainable-computing-io/kepler-operator/issues)中创建问题
