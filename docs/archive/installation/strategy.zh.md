# 安装策略

虽然您可以自由探索任何部署方式，但推荐的策略如下：

| *OCP 4.13*      | *Microshift*     | *RHEL*  |  *ROSA* | *Kind* |
| ------------- | -------------  | ----- | ----- | ----|
| kepler-operator | Manifests  | RPM | Manifests | Helm Charts, Manifests, kepler-operator|

## 要求

- 内核 4.18+
- `kubectl` v1.21.0+
- 默认以非 root 用户安装 `docker`
