# ⚙️ Kepler 配置指南

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

Kepler 支持通过命令行标志和配置文件进行配置。本指南概述了配置 Kepler 的所有可用配置选项。

## 🛠️ 配置方法

Kepler 支持两种主要的配置方法：

1. **命令行标志**：用于快速调整和一次性设置
2. **配置文件**：用于持久和全面的配置

> ⚡ **提示：** 当同时指定命令行标志和配置文件设置时，命令行标志优先。

## 🖥️ 命令行标志

您可以通过在启动服务时传递标志来配置 Kepler。以下标志可用：

| 标志 | 描述 | 默认值 | 值 |
|------|-------------|---------|--------|
| `--config.file` | YAML 配置文件路径 | | 任何有效的文件路径 |
| `--log.level` | 日志级别 | `info` | `debug`, `info`, `warn`, `error` |
| `--log.format` | 日志输出格式 | `text` | `text`, `json` |
| `--host.sysfs` | sysfs 文件系统路径 | `/sys` | 任何有效的目录路径 |
| `--host.procfs` | procfs 文件系统路径 | `/proc` | 任何有效的目录路径 |
| `--monitor.interval` | 监控刷新间隔 | `5s` | 任何有效的持续时间 |
| `--monitor.max-terminated` | 在导出前保存在内存中的已终止工作负载的最大数量 | `500` | 负数表示 `unlimited`，`0` 禁用此功能 |
| `--web.config-file` | TLS 服务器配置文件路径 | `""` | 任何有效的文件路径 |
| `--web.listen-address` | Web 服务器监听地址（可多次指定） | `:28282` | 任何有效的 host:port 或 :port 格式 |
| `--debug.pprof` | 启用 pprof 调试端点 | `false` | `true`, `false` |
| `--exporter.stdout` | 启用 stdout 导出器 | `false` | `true`, `false` |
| `--exporter.prometheus` | 启用 Prometheus 导出器 | `true` | `true`, `false` |
| `--metrics` | 要导出的指标级别（可多次指定） | `node,process,container,vm,pod` | `node`, `process`, `container`, `vm`, `pod` |
| `--kube.enable` | 监控 kubernetes | `false` | `true`, `false` |
| `--kube.config` | kubeconfig 文件路径 | `""` | 任何有效的文件路径 |
| `--kube.node-name` | 运行 kepler 的 kubernetes 节点名称 | `""` | 任何有效的节点名称 |

### 💡 示例

```bash
# 使用调试日志级别运行
kepler --log.level=debug

# 使用不同的 procfs 路径和 JSON 日志
kepler --host.procfs=/custom/proc --log.format=json

# 从文件加载配置
kepler --config.file=/path/to/config.yaml

# 使用自定义监听地址
kepler --web.listen-address=:8080 --web.listen-address=localhost:9090

# 启用 stdout 导出器并禁用 Prometheus 导出器
kepler --exporter.stdout=true --exporter.prometheus=false

# 启用 Kubernetes 监控并指定 kubeconfig 和节点名称
kepler --kube.enable=true --kube.config=/path/to/kubeconfig --kube.node-name=my-node

# 仅导出节点和容器级别指标
kepler --metrics=node --metrics=container

# 仅导出进程级别指标
kepler --metrics=process

# 将最大已终止工作负载设置为 1000
kepler --monitor.max-terminated=1000

# 禁用已终止工作负载跟踪
kepler --monitor.max-terminated=0

# 无限制已终止工作负载跟踪
kepler --monitor.max-terminated=-1
```

## 🗂️ 配置文件

Kepler 可以从 YAML 文件加载配置。配置文件提供比命令行标志更广泛的选项。

### 🧾 示例配置文件

```yaml
log:
  level: debug  # debug, info, warn, error (默认: info)
  format: text  # text 或 json (默认: text)

monitor:
  interval: 5s        # 监控刷新间隔 (默认: 5s)
  staleness: 500ms    # 数据被认为过时的持续时间 (默认: 500ms)
  maxTerminated: 500  # 在内存中保存已终止工作负载的最大数量 (默认: 500)
  minTerminatedEnergyThreshold: 10  # 已终止工作负载的最低能量阈值 (默认: 10)

host:
  sysfs: /sys   # sysfs 文件系统路径 (默认: /sys)
  procfs: /proc # procfs 文件系统路径 (默认: /proc)

rapl:
  zones: []     # 要启用的 RAPL 区域，空值启用所有默认区域

exporter:
  stdout:       # stdout 导出器相关配置
    enabled: false # 默认禁用
  prometheus:   # prometheus 导出器相关配置
    enabled: true
    debugCollectors:
      - go
      - process
    metricsLevel:
      - node
      - process
      - container
      - vm
      - pod

debug:          # 调试相关配置
  pprof:        # pprof 相关配置
    enabled: true

web:
  configFile: "" # TLS 服务器配置文件路径
  listenAddresses: # Web 服务器监听地址
    - ":28282"

kube:           # kubernetes 相关配置
  enabled: false    # 启用 kubernetes 监控 (默认: false)
  config: ""        # kubeconfig 文件路径 (在集群内运行时可选)
  nodeName: ""      # kubernetes 节点名称 (启用时必需)

# 警告：请勿在生产环境中启用 - 仅用于开发/测试
dev:
  fake-cpu-meter:
    enabled: false
    zones: []  # 要启用的区域，空值启用所有默认区域
```

## 🧩 详细配置选项

### 📝 日志配置

```yaml
log:
  level: info   # 日志级别
  format: text  # 输出格式
```

- **level**：控制日志的详细程度
  - `debug`：非常详细，包含详细的操作信息
  - `info`：标准操作信息
  - `warn`：仅警告和错误
  - `error`：仅错误

- **format**：控制日志的输出格式
  - `text`：人类可读格式
  - `json`：JSON 格式，适用于日志处理系统

### 📊 监控配置

```yaml
monitor:
  interval: 5s
  staleness: 500ms
  maxTerminated: 500
  minTerminatedEnergyThreshold: 10
```

- **interval**：监控的刷新间隔。生命周期少于此间隔的所有进程将被忽略。设置为 0s 禁用监控刷新。

- **staleness**：监控器计算的数据被认为过时并在再次请求时重新计算的持续时间。在多个 Prometheus 实例抓取 Kepler 时特别有用，确保它们在过时窗口内接收相同的数据。应短于监控间隔。

- **maxTerminated**：在数据导出前在内存中保存已终止工作负载（进程、容器、虚拟机、Pod）的最大数量。这防止了在高流失环境中的无限内存增长。设置为 0 禁用。达到限制时，首先移除功耗最低的已终止工作负载。

- **minTerminatedEnergyThreshold**：已终止工作负载跟踪的最低能耗阈值（以焦耳为单位）。只有能耗高于此阈值的已终止工作负载才会被包含在跟踪中。这有助于过滤掉消耗最少能量的短期进程。默认为 10 焦耳。

### 🗄️ 主机配置

```yaml
host:
  sysfs: /sys    # sysfs 路径
  procfs: /proc  # procfs 路径
```

这些设置指定 Kepler 应该在哪里查找系统信息。在容器化环境中，您可能需要调整这些路径。

### 🔋 RAPL 区域配置

```yaml
rapl:
  zones: []  # 要启用的 RAPL 区域
```

运行平均功率限制（RAPL）是 Intel 的功率限制机制。默认情况下，Kepler 启用所有可用区域。您可以通过列出特定区域来限制。

具体区域示例：

```yaml
rapl:
  zones: ["package", "core", "uncore"]
```

### 📦 导出器配置

```yaml
exporter:
  stdout:       # stdout 导出器相关配置
    enabled: false # 默认禁用
  prometheus:   # prometheus 导出器相关配置
    enabled: true
    debugCollectors:
      - go
      - process
    metricsLevel:
      - node
      - process
      - container
      - vm
      - pod
```

- **stdout**：stdout 导出器配置
  - `enabled`：启用或禁用 stdout 导出器（默认：false）

- **prometheus**：Prometheus 导出器配置
  - `enabled`：启用或禁用 Prometheus 导出器（默认：true）
  - `debugCollectors`：要启用的调试收集器列表（可用："go"、"process"）
  - `metricsLevel`：要公开的指标级别列表。控制导出指标的粒度：
    - `node`：节点级指标（系统范围的功耗）
    - `process`：进程级指标（每个进程的功耗）
    - `container`：容器级指标（每个容器的功耗）
    - `vm`：虚拟机级指标（每个虚拟机的功耗）
    - `pod`：Pod 级指标（Kubernetes 中每个 Pod 的功耗）

### 🐞 调试配置

```yaml
debug:
  pprof:
    enabled: true
```

- **pprof**：pprof 调试配置
  - `enabled`：启用时，这会公开可用于分析 Kepler 的 [pprof](https://golang.org/pkg/net/http/pprof/) 调试端点（默认：true）

### 🌐 Web 配置

```yaml
web:
  configFile: ""  # TLS 服务器配置文件路径
  listenAddresses: # Web 服务器监听地址
    - ":28282"
```

- **configFile**：用于保护 Kepler Web 端点的 TLS 服务器配置文件路径
- **listenAddresses**：Web 服务器应监听的地址列表（默认：[":28282"]）
  - 支持 host:port 格式（例如，"localhost:8080"、"0.0.0.0:9090"）和仅端口格式（例如，":8080"）
  - 可以指定多个地址以在不同接口或端口上监听
  - 支持使用括号表示法的 IPv6 地址（例如，"[::1]:8080"）

TLS 服务器配置文件内容示例：

```yaml
# TLS 服务器配置
tls_server_config:
  cert_file: /path/to/cert.pem  # 证书文件路径
  key_file: /path/to/key.pem    # 密钥文件路径
```

### 🐳 Kubernetes 配置

```yaml
kube:
  enabled: false    # 启用 kubernetes 监控
  config: ""        # kubeconfig 文件路径
  nodeName: ""      # kubernetes 节点名称
```

- **enabled**：启用或禁用 Kubernetes 监控（默认：false）
  - 启用时，Kepler 将监控 Kubernetes 资源并公开 Pod 级别信息

- **config**：kubeconfig 文件路径（可选）
  - 在 Kubernetes 集群外运行 Kepler 时必需
  - 在集群内运行时，Kepler 可以使用集群内配置
  - 必须是有效且可读的 kubeconfig 文件

- **nodeName**：运行 Kepler 的 Kubernetes 节点名称（启用时必需）
  - 这有助于 Kepler 识别它正在监控的节点
  - 必须与 Kubernetes 集群中的实际节点名称匹配
  - 当 `enabled` 设置为 `true` 时必需

### 🧑‍🔬 开发配置

```yaml
dev:
  fake-cpu-meter:
    enabled: false
    zones: []
```

⚠️ **警告**：此部分仅用于开发和测试。请勿在生产环境中启用。

- **fake-cpu-meter**：启用时，使用假 CPU 计量器而不是真实硬件指标
  - `enabled`：设置为 `true` 启用假 CPU 计量器
  - `zones`：要启用的特定区域，空值启用所有区域

## 📖 延伸阅读

更多详细信息，请参阅主 Kepler 仓库中 `hack/config.yaml` 的配置文件示例

配置愉快！🎉
