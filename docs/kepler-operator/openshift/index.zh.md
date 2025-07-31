# OpenShift 上的 Kepler Operator

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

## 概述

Kepler Operator 提供了一种在 OpenShift 集群上部署和管理 Kepler（Kubernetes 高效功率级别导出器）的简化方式。该 operator 使用现代的 PowerMonitor 自定义资源定义来提供增强的配置选项和改进的资源管理。

## 迁移通知

!!! warning "重要"
    Kepler CRD 已弃用并将在未来版本中删除。请为所有新部署使用 PowerMonitor，并迁移现有安装以确保持续支持。

## 先决条件

在安装 Kepler Operator 之前，确保您具有：

- 具有 `cluster-admin` 权限的 OpenShift 集群访问权限
- 在集群中启用用户工作负载监控
- 访问 OperatorHub（用于 UI 安装）
- 安装了 `oc` CLI 工具（用于命令行操作）

!!! note
    您的 operator 将自动使用 kubeconfig 文件中的当前上下文（即 `oc cluster-info` 显示的任何集群）。

## 安装选项

选择最适合您工作流程的安装方法：

### [快速入门指南](quickstart.zh.md)（推荐）

最适合新接触 Kepler Operator 并希望使用 OpenShift Web 控制台快速启动和运行的用户。

- 通过 OperatorHub 安装
- 创建基本 PowerMonitor 实例
- 验证安装
- 访问初始指标

### [CLI 安装指南](cli-installation.zh.md)

非常适合自动化、脚本编写或偏好命令行工作流程的用户。

- 通过命令行安装 operator
- 使用 YAML 部署 PowerMonitor
- 验证命令
- 脚本示例

## 安装后

一旦安装了 operator，请探索这些指南：

### [配置指南](../configuration/index.zh.md)

了解如何自定义您的 Kepler 部署：

- 指标级别和采样率
- 安全配置
- 资源管理
- 节点选择和容忍度
- 高级配置选项

### [监控和故障排除](../configuration/monitoring-troubleshooting.zh.md)

设置监控和解决常见问题：

- 用户工作负载监控设置
- OpenShift 指标仪表板
- Grafana 集成
- 常见故障排除场景

## 迁移

### [迁移指南](../migration/index.zh.md)

如果您正在从已弃用的 Kepler CRD 升级：

- 逐步迁移过程
- 配置对比
- 回滚程序

## 获取帮助

- [项目资源](../../project/resources.zh.md) - 其他文档和资源
- [支持](../../project/support.zh.md) - 社区支持和贡献指南
