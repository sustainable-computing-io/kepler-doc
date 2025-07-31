# CLI 安装指南

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

本指南展示了如何使用 OpenShift 命令行界面安装 Kepler Operator 并创建 PowerMonitor 实例。这种方法非常适合自动化、脚本编写和偏好基于终端工作流程的用户。

## 先决条件

确保您具有：

- 已安装并配置的 `oc` CLI 工具
- OpenShift 集群上的集群管理员权限
- 当前上下文指向目标集群（`oc cluster-info`）

## 步骤 1：安装 Operator

### 创建 Operator 订阅

从社区目录安装 Kepler Operator：

```bash
oc apply -f - << EOF
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: kepler-operator
  namespace: openshift-operators
spec:
  channel: alpha
  name: kepler-operator
  source: community-operators
  sourceNamespace: openshift-marketplace
EOF
```

### 验证安装

等待 operator 准备就绪：

```bash
# 检查订阅状态
oc get subscription kepler-operator -n openshift-operators

# 检查 ClusterServiceVersion (CSV)
oc get csv -n openshift-operators | grep kepler

# 等待 operator pod 运行
oc get pods -n openshift-operators | grep kepler-operator
```

准备就绪时的预期输出：

```text
kepler-operator-controller-manager-xxx   2/2     Running   0   2m
```

## 步骤 2：创建 PowerMonitor 实例

### 基本 PowerMonitor 配置

使用默认设置创建 PowerMonitor：

```bash
oc apply -f - << EOF
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
      staleness: 500ms
      maxTerminated: 500
    deployment:
      security:
        mode: none
EOF
```

### 验证 PowerMonitor 部署

检查 PowerMonitor 是否已创建并正常运行：

```bash
# 检查 PowerMonitor 状态
oc get powermonitor power-monitor -o wide

# 检查条件
oc describe powermonitor power-monitor

# 验证 DaemonSet 创建
oc get daemonset -n power-monitor

# 检查所有节点上的 pod
oc get pods -n power-monitor -o wide
```

## 步骤 3：验证命令

### 检查 Operator 健康状态

```bash
# Operator pod 状态
oc get pods -n openshift-operators | grep kepler-operator

# Operator 日志
oc logs -n openshift-operators deployment/kepler-operator-controller-manager
```

### 检查 PowerMonitor 资源

```bash
# PowerMonitor 状态和条件
oc get powermonitor power-monitor -o yaml

# DaemonSet 详情
oc describe daemonset -n power-monitor

# Pod 日志
oc logs -n power-monitor -l app.kubernetes.io/name=kepler-exporter
```

### 测试指标端点

```bash
# 端口转发到指标端点
oc port-forward -n power-monitor svc/kepler-exporter 9102:9102 &

# 测试指标（在另一个终端中）
curl http://localhost:9102/metrics | head -20

# 停止端口转发
pkill -f "port-forward.*9102"
```

## 自动化脚本

### 完整安装脚本

将此保存为 `install-kepler-operator.sh`：

```bash
#!/bin/bash
set -e

echo "Installing Kepler Operator..."

# 安装 operator
oc apply -f - << EOF
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: kepler-operator
  namespace: openshift-operators
spec:
  channel: alpha
  name: kepler-operator
  source: community-operators
  sourceNamespace: openshift-marketplace
EOF

echo "Waiting for operator to be ready..."
while ! oc get csv -n openshift-operators | grep -q kepler.*Succeeded; do
  echo "Waiting for CSV to be ready..."
  sleep 10
done

echo "Creating PowerMonitor instance..."
oc apply -f - << EOF
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
      security:
        mode: none
EOF

echo "Waiting for DaemonSet to be ready..."
while ! oc get daemonset -n power-monitor 2>/dev/null | grep -q kepler; do
  echo "Waiting for DaemonSet creation..."
  sleep 5
done

echo "Installation complete!"
echo "Check status with: oc get powermonitor power-monitor"
```

使其可执行并运行：

```bash
chmod +x install-kepler-operator.sh
./install-kepler-operator.sh
```

### 卸载脚本

将此保存为 `uninstall-kepler-operator.sh`：

```bash
#!/bin/bash
set -e

echo "Removing PowerMonitor instance..."
oc delete powermonitor power-monitor --ignore-not-found=true

echo "Waiting for resources cleanup..."
sleep 10

echo "Removing operator subscription..."
oc delete subscription kepler-operator -n openshift-operators --ignore-not-found=true

echo "Removing CSV..."
oc delete csv -n openshift-operators $(oc get csv -n openshift-operators -o name | grep kepler) --ignore-not-found=true

echo "Uninstall complete!"
```

## 配置文件

对于生产部署，将配置保存到文件：

### powermonitor-basic.yaml

```yaml
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
```

### powermonitor-production.yaml

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
      staleness: 1s
      maxTerminated: 1000
    deployment:
      security:
        mode: rbac
      nodeSelector:
        kubernetes.io/os: linux
      tolerations:
      - key: node-role.kubernetes.io/master
        operator: Exists
        effect: NoSchedule
```

使用以下命令应用：

```bash
oc apply -f powermonitor-production.yaml
```

## 后续步骤

- **[配置指南](../configuration/index.zh.md)** - 高级配置选项
- **[监控设置](../configuration/monitoring-troubleshooting.zh.md)** - 设置监控和故障排除
