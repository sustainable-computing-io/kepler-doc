# ⚙️ Kepler 配置指南

Kepler支持通过命令行参数和配置文件两种方式进行配置。本指南详细介绍了所有可用的配置选项。

## 🛠️ 配置方法

Kepler支持两种主要配置方式：

1. **命令行参数**：用于快速调整和一次性设置
2. **配置文件**：用于持久化和全面配置

> ⚡ **提示**：当同时指定两者时，命令行参数优先级高于配置文件设置。

## 🖥️ 命令行参数

启动服务时可通过以下参数配置Kepler：

| 参数 | 描述 | 默认值 | 可选值 |
|------|-------------|---------|--------|
| `--config.file` | YAML配置文件路径 | | 任意有效文件路径 |
| `--log.level` | 日志级别 | `info` | `debug`, `info`, `warn`, `error` |
| `--log.format` | 日志输出格式 | `text` | `text`, `json` |
| `--host.sysfs` | sysfs文件系统路径 | `/sys` | 任意有效目录路径 |
| `--host.procfs` | procfs文件系统路径 | `/proc` | 任意有效目录路径 |
| `--monitor.interval` | 监控刷新间隔 | `5s` | 任意有效时长 |
| `--monitor.max-terminated` | 内存中保留的终止工作负载最大数量 | `500` | 负数表示`无限制`，`0`表示禁用该功能 |
| `--web.config-file` | TLS服务器配置文件路径 | `""` | 任意有效文件路径 |
| `--web.listen-address` | 网络服务监听地址（可多次指定） | `:28282` | 任意有效的host:port或:port格式 |
| `--debug.pprof` | 启用pprof调试端点 | `false` | `true`, `false` |
| `--exporter.stdout` | 启用标准输出导出器 | `false` | `true`, `false` |
| `--exporter.prometheus` | 启用Prometheus导出器 | `true` | `true`, `false` |
| `--metrics` | 导出指标级别（可多次指定） | `node,process,container,vm,pod` | `node`, `process`, `container`, `vm`, `pod` |
| `--kube.enable` | 监控Kubernetes | `false` | `true`, `false` |
| `--kube.config` | kubeconfig文件路径 | `""` | 任意有效文件路径 |
| `--kube.node-name` | Kepler运行的Kubernetes节点名称 | `""` | 任意有效节点名称 |

### 💡 示例

```bash
# 启用调试日志
kepler --log.level=debug

# 使用自定义procfs路径和JSON日志格式
kepler --host.procfs=/custom/proc --log.format=json

# 从配置文件加载配置
kepler --config.file=/path/to/config.yaml

# 使用自定义监听地址
kepler --web.listen-address=:8080 --web.listen-address=localhost:9090

# 启用标准输出导出器并禁用Prometheus导出器
kepler --exporter.stdout=true --exporter.prometheus=false

# 启用Kubernetes监控并指定kubeconfig和节点名称
kepler --kube.enable=true --kube.config=/path/to/kubeconfig --kube.node-name=my-node

# 仅导出节点和容器级别指标
kepler --metrics=node --metrics=container

# 仅导出进程级别指标
kepler --metrics=process

# 设置最大终止工作负载数为1000
kepler --monitor.max-terminated=1000

# 禁用终止工作负载追踪
kepler --monitor.max-terminated=0

# 无限终止工作负载追踪
kepler --monitor.max-terminated=-1
```

## 🗂️ 配置文件

Kepler可以从YAML文件加载配置，配置文件提供比命令行参数更全面的选项。

### 🧾 配置文件示例

```yaml
log:
  level: debug  # 日志级别：debug, info, warn, error (默认: info)
  format: text  # 输出格式：text 或 json (默认: text)

monitor:
  interval: 5s        # 监控刷新间隔 (默认: 5s)
  staleness: 1000ms   # 数据过期时间 (默认: 1000ms)
  maxTerminated: 500  # 内存中保留的终止工作负载最大数量 (默认: 500)
  minTerminatedEnergyThreshold: 10  # 终止工作负载的最小能量阈值 (默认: 10)

host:
  sysfs: /sys   # sysfs文件系统路径 (默认: /sys)
  procfs: /proc # procfs文件系统路径 (默认: /proc)

rapl:
  zones: []     # 启用的RAPL区域，空值启用所有默认区域

exporter:
  stdout:       # 标准输出导出器配置
    enabled: false # 默认禁用
  prometheus:   # Prometheus导出器配置
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

debug:          # 调试配置
  pprof:        # pprof配置
    enabled: true

web:
  configFile: "" # TLS服务器配置文件路径
  listenAddresses: # 网络服务监听地址
    - ":28282"

kube:           # Kubernetes配置
  enabled: false    # 启用Kubernetes监控 (默认: false)
  config: ""        # kubeconfig文件路径 (集群内运行时可选)
  nodeName: ""      # Kubernetes节点名称 (启用时必填)

# 警告：生产环境请勿启用 - 仅用于开发测试
dev:
  fake-cpu-meter:
    enabled: false
    zones: []  # 启用的区域，空值启用所有默认区域
```

## 🧩 配置选项详解

### 📝 日志配置

```yaml
log:
  level: info   # 日志级别
  format: text  # 输出格式
```

- **level**: 控制日志详细程度
  - `debug`: 非常详细，包含操作细节
  - `info`: 标准操作信息
  - `warn`: 仅警告和错误
  - `error`: 仅错误信息

- **format**: 控制日志输出格式
  - `text`: 人类可读格式
  - `json`: JSON格式，适合日志处理系统

### 📊 监控配置

```yaml
monitor:
  interval: 5s
  staleness: 1000ms
  maxTerminated: 500
  minTerminatedEnergyThreshold: 10
```

- **interval**: 监控刷新间隔。生命周期短于此间隔的进程将被忽略。设为0s将禁用监控刷新。

- **staleness**: 监控数据过期时间。特别适用于多个Prometheus实例抓取Kepler的情况，确保在过期窗口内收到相同数据。应短于监控间隔。

- **maxTerminated**: 内存中保留的终止工作负载(进程/容器/虚拟机/Pod)最大数量。设为0禁用。达到限制时，优先移除能耗最低的终止工作负载。

- **minTerminatedEnergyThreshold**: 终止工作负载的最小能量消耗阈值(焦耳)。仅跟踪超过此阈值的终止工作负载，可过滤短生命周期进程。默认10焦耳。

### 🗄️ 主机配置

```yaml
host:
  sysfs: /sys    # sysfs路径
  procfs: /proc  # procfs路径
```

指定系统信息查找路径。容器环境中可能需要调整这些路径。

### 🔋 RAPL区域配置

```yaml
rapl:
  zones: []  # 启用的RAPL区域
```

RAPL(Running Average Power Limit)是Intel的功耗限制机制。默认启用所有可用区域，可通过列表限制特定区域。

示例指定区域：

```yaml
rapl:
  zones: ["package", "core", "uncore"]
```

### 📦 导出器配置

```yaml
exporter:
  stdout:       # 标准输出导出器
    enabled: false # 默认禁用
  prometheus:   # Prometheus导出器
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

- **stdout**: 标准输出导出器配置
  - `enabled`: 启用/禁用(默认: false)

- **prometheus**: Prometheus导出器配置
  - `enabled`: 启用/禁用(默认: true)
  - `debugCollectors`: 启用的调试收集器(可选: "go", "process")
  - `metricsLevel`: 导出的指标级别：
    - `node`: 节点级(系统整体功耗)
    - `process`: 进程级
    - `container`: 容器级
    - `vm`: 虚拟机级
    - `pod`: Kubernetes Pod级

### 🐞 调试配置

```yaml
debug:
  pprof:
    enabled: true
```

- **pprof**: 启用后暴露[pprof](https://golang.org/pkg/net/http/pprof/)调试端点(默认: true)

### 🌐 网络配置

```yaml
web:
  configFile: ""  # TLS服务器配置文件路径
  listenAddresses: # 监听地址
    - ":28282"
```

- **configFile**: TLS服务器配置文件路径
- **listenAddresses**: 网络服务监听地址列表(默认: [":28282"])
  - 支持host:port格式(如"localhost:8080")和纯端口格式(如":8080")
  - 可指定多个地址监听不同接口
  - 支持IPv6地址(如"[::1]:8080")

TLS配置文件示例内容：

```yaml
tls_server_config:
  cert_file: /path/to/cert.pem  # 证书文件路径
  key_file: /path/to/key.pem    # 密钥文件路径
```

### 🐳 Kubernetes配置

```yaml
kube:
  enabled: false    # 启用Kubernetes监控
  config: ""        # kubeconfig文件路径
  nodeName: ""      # 节点名称
```

- **enabled**: 启用/禁用Kubernetes监控(默认: false)
- **config**: kubeconfig文件路径
  - 集群外运行时必需
  - 集群内可使用集群内配置
- **nodeName**: Kepler运行的节点名称(启用时必填)

### 🧑‍🔬 开发配置

```yaml
dev:
  fake-cpu-meter:
    enabled: false
    zones: []
```

⚠️ **警告**：仅用于开发和测试，生产环境请勿启用。

- **fake-cpu-meter**: 启用模拟CPU计量器
  - `enabled`: 设为`true`启用
  - `zones`: 指定区域，空值启用所有

## 📖 延伸阅读

更多细节请参考Kepler主仓库中的示例配置文件：`hack/config.yaml`

祝您配置愉快！🎉