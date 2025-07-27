# 开发者文档

## 📍 开发者文档位置

Kepler 及相关项目的开发者文档维护在各项目的代码仓库中，位于 `docs/developer/` 目录下。

## 🔗 Kepler 开发者文档

完整开发者文档包含架构设计、开发流程、测试策略和贡献指南等内容，请访问：

**🚀 [Kepler 开发者文档](https://github.com/sustainable-computing-io/kepler/tree/main/docs/developer)**

### 您将找到以下内容

- **架构概述** - 面向服务的设计模式与组件结构
- **开发环境配置** - Docker Compose、本地构建与测试
- **能耗归因指南** - 深入解析能耗测量与归因算法
- **预提交钩子** - 代码质量与自动化检查配置
- **发布流程** - 版本创建与管理规范
- **测试策略** - 单元测试、集成测试与竞态检测
- **服务接口** - 理解服务框架与生命周期管理
- **配置管理** - YAML 层级结构与 CLI 参数系统

## 🛠️ 快速开发者配置

快速开始开发的命令如下：

```bash
# 克隆并构建
git clone https://github.com/sustainable-computing-io/kepler.git
cd kepler
make build

# 使用 Docker Compose 开发（包含 Grafana + Prometheus）
cd compose/dev
docker-compose up -d

# 运行测试
make test

# 本地开发
sudo ./bin/kepler --config hack/config.yaml
```

## 📚 相关项目文档

Kepler 生态系统中其他项目的文档请查阅对应仓库：

- **Kepler Operator**: [sustainable-computing-io/kepler-operator](https://github.com/sustainable-computing-io/kepler-operator)
- **Kepler 模型服务器**: [sustainable-computing-io/kepler-model-server](https://github.com/sustainable-computing-io/kepler-model-server)

## 🤝 贡献指南

向 Kepler 贡献代码前请查阅：

1. **[开发者文档](https://github.com/sustainable-computing-io/kepler/tree/main/docs/developer)** - 技术实现细节
2. **[贡献指南](../project/contributing.md)** - 通用贡献流程
3. **[行为准则](https://github.com/sustainable-computing-io/kepler/blob/main/CODE_OF_CONDUCT.md)** - 社区规范

## 💬 开发者支持

- **GitHub Issues**: [报告缺陷或功能请求](https://github.com/sustainable-computing-io/kepler/issues)
- **GitHub Discussions**: [提问与分享想法](https://github.com/sustainable-computing-io/kepler/discussions)
- **Slack 频道**: [CNCF Slack 中的 #kepler 频道](https://cloud-native.slack.com/archives/C06HYDN4A01)

---

*开发者文档在项目仓库中持续维护，以确保与代码库保持同步更新。*