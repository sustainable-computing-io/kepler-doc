# 安装策略

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

虽然您可以自由探索任何部署方式，但推荐的策略如下：

| *OCP 4.13*      | *Microshift*     | *RHEL*  |  *ROSA* | *Kind* |
| ------------- | -------------  | ----- | ----- | ----|
| kepler-operator | Manifests  | RPM | Manifests | Helm Charts, Manifests, kepler-operator|

## 要求

- 内核 4.18+
- `kubectl` v1.21.0+
- 默认以非 root 用户安装 `docker`
