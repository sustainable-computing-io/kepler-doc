# Kepler Model Server 兼容性通知

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

⚠️ **兼容性警告** ⚠️

## Kepler v0.10.0+ 的 Model Server 状态

**Kepler Model Server 不兼容** Kepler v0.10.0 及以上版本，这是由于重大架构重写造成的。本节中的 Model Server 文档**仅适用于 Kepler v0.9.0 及以下版本**。

## v0.10.0 中的更改

Kepler v0.10.0 引入了破坏 Model Server 兼容性的根本性变化：

### 指标结构变化

- **旧版**：复杂的基于组件的指标（core、uncore、package、DRAM、GPU）
- **新版**：简化的以 CPU 为重点的指标，采用基于区域的组织方式
- **影响**：Model Server 期望旧的指标名称和结构

### 功率归因变化

- **旧版**：基于硬件计数器的归因，具有详细的组件分解
- **新版**：基于 CPU 时间比例的归因，具有活动/空闲分割
- **影响**：模型训练数据格式和归因逻辑不兼容

### 配置系统变化

- **旧版**：基于环境变量的配置，Model Server 与之集成
- **新版**：CLI 标志 + YAML 层次结构，具有不同的配置结构
- **影响**：Model Server 配置集成不再工作

## 当前状态

🔴 **不工作**：Model Server 与 Kepler v0.10.0+ 的集成

🟡 **审查中**：兼容性评估和潜在更新

🔵 **未来计划**：可能为未来版本计划 Model Server 更新

## 对于旧版用户

如果您需要使用 Model Server：

1. **使用 Kepler v0.9.0 或以下版本**，采用旧架构
2. **参考存档文档**以了解正确的设置程序
3. **查看[存档部分](archive/README.zh.md)**以获得旧版安装指南

## 替代解决方案

对于需要功率建模的 Kepler v0.10.0+ 用户：

1. **直接指标导出**：直接使用简化的指标进行分析
2. **自定义集成**：使用新的指标结构构建自定义解决方案
3. **等待更新**：监控项目以获得 Model Server 兼容性更新

## 保持更新

- **GitHub Issues**：关注 Model Server 兼容性更新
- **社区讨论**：参与关于 Model Server 未来的讨论
- **发布说明**：查看未来发布说明以获得兼容性公告

---

⚠️ **不要尝试将 Model Server 文档与 Kepler v0.10.0+ 一起使用**，
因为这将导致配置错误和不兼容的集成。
