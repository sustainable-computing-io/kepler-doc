# 安装策略

您可以自由探索任何部署方式，但推荐策略如下：

| *OCP 4.13*      | *Microshift*     | *RHEL*  |  *ROSA* | *Kind* |
| ------------- | -------------  | ----- | ----- | ----|
| kepler-operator | 清单文件  | RPM包 | 清单文件 | Helm图表、清单文件、kepler-operator|

## 要求

- 内核版本 4.18+
- `kubectl` v1.21.0+ 版本
- 默认以非root用户安装的 `docker`

（说明：保持Kepler英文不变，保留Markdown表格格式，技术术语如RPM/Helm等采用通用译法，"Manifests"译为"清单文件"符合K8s中文社区习惯，版本号格式保持不变）