# 故障排除

## Kepler Pod 启动失败

### 背景

Kepler 使用 eBPF 获取性能计数器读数和进程统计信息。由于 eBPF 需要内核头文件，
当内核头文件缺失时，Kepler 将无法启动。

### 诊断

要确认，请使用以下命令检查 Kepler Pod 日志并查找消息
`not able to load eBPF modules`。

```bash
kubectl logs -n kepler daemonset/kepler-exporter
```

### 解决方案

可以使用以下命令在每个节点上手动安装内核头文件

```bash
# 基于 Fedora/RHEL 的发行版
dnf install kernel-devel-`uname -r` -y
# Debian/Ubuntu 发行版
apt install linux-headers-$(uname -r)
```

在 OpenShift 上，安装[这里](https://github.com/sustainable-computing-io/kepler/tree/main/manifests/config/cluster-prereqs)的 MachineConfiguration
