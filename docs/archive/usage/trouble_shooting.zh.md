# 故障排除

## Kepler Pod 启动失败

### 背景

Kepler 使用 eBPF 技术获取性能计数器读数并处理统计信息。由于 eBPF 需要内核头文件支持，当内核头文件缺失时会导致 Kepler 启动失败。

### 诊断方法

执行以下命令检查 Kepler Pod 日志，确认是否存在 `not able to load eBPF modules` 错误信息：

```bash
kubectl logs -n kepler daemonset/kepler-exporter
```

### 解决方案

在每个节点上手动安装内核头文件，具体命令如下：

```bash
# Fedora/RHEL 系列发行版
dnf install kernel-devel-`uname -r` -y
# Debian/Ubuntu 系列发行版
apt install linux-headers-$(uname -r)
```

在 OpenShift 环境中，请安装 [MachineConfiguration](https://github.com/sustainable-computing-io/kepler/tree/main/manifests/config/cluster-prereqs)