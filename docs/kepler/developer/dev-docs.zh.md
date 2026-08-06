# 开发者文档

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

## 📍 开发者文档位置

Kepler 和相关项目的开发者文档在每个项目的仓库中的 `docs/developer/` 目录下维护。

## 🔗 Kepler 开发者文档

有关包括架构、开发工作流程、测试策略和贡献指南在内的全面开发者文档，请访问：

**🚀 [Kepler 开发者文档](https://github.com/sustainable-computing-io/kepler/tree/main/docs/developer)**

### 您将在那里找到什么

- **架构概述** - 面向服务的设计模式和组件结构
- **开发环境设置** - Docker Compose、本地构建和测试
- **功率归因指南** - 深入了解能量测量和归因算法
- **Pre-commit Hook** - 代码质量和自动检查设置
- **发布工作流程** - 如何创建和管理发布版本
- **测试策略** - 单元测试、集成测试和竞态检测
- **服务接口** - 理解服务框架和生命周期管理
- **配置管理** - YAML 层次结构和 CLI 标志系统

## 🛠️ 快速开发者设置

对于即时开发设置，关键命令如下：

```bash
# 克隆和构建
git clone https://github.com/sustainable-computing-io/kepler.git
cd kepler
make build

# 使用 Docker Compose 开发（包括 Grafana + Prometheus）
cd compose/dev
docker compose up -d

# 运行测试
make test

# 本地开发
sudo ./bin/kepler --config.file hack/config.yaml
```

## 📚 相关项目文档

对于 Kepler 生态系统中的其他项目，请查看其各自的仓库：

- **Kepler Operator**: [sustainable-computing-io/kepler-operator](https://github.com/sustainable-computing-io/kepler-operator)
- **Kepler Model Server**: [sustainable-computing-io/kepler-model-server](https://github.com/sustainable-computing-io/kepler-model-server)

## 🤝 贡献

在为 Kepler 贡献之前，请查看：

1. **[开发者文档](https://github.com/sustainable-computing-io/kepler/tree/main/docs/developer)** - 技术实现细节
2. **[贡献指南](../../project/contributing.zh.md)** - 一般贡献流程
3. **[行为准则](https://github.com/sustainable-computing-io/kepler/blob/main/code-of-conduct.md)** - 社区准则

## 💬 开发者支持

- **GitHub Issues**: [报告错误或请求功能](https://github.com/sustainable-computing-io/kepler/issues)
- **GitHub Discussions**: [提问和分享想法](https://github.com/sustainable-computing-io/kepler/discussions)
- **Slack 频道**: [CNCF Slack 中的 #kepler](https://cloud-native.slack.com/archives/C06HYDN4A01)
- **社区会议录像**:
  - [youtube](https://youtube.com/playlist?list=PL8-Q56LqwwAjox1MSt8VzviKO-PBD4zue&si=pJhOwkatydv3-c1t)
  - [bilibili](https://space.bilibili.com/276546/lists/2476604), 如果你没有Youtube访问方式

---

*开发者文档在项目仓库中积极维护，以确保与代码库保持同步。*
