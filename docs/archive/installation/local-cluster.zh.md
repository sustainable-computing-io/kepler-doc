# 本地集群设置

Kepler 运行于 Kubernetes 环境。若您已拥有可用集群，可跳过本节内容。如需部署本地集群，推荐使用 [kind](https://kind.sigs.k8s.io/)。`kind` 是通过 Docker 容器"节点"运行本地 Kubernetes 集群的工具，虽最初为测试 Kubernetes 本身设计，但同样适用于本地开发或持续集成场景。

## 安装 kind

安装 `kind` 请[参阅此处说明](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)。

需对集群进行特定配置以支持 Kepler 运行，关键要挂载两个主机目录：
- `/proc`（用于暴露主机进程信息）
- `/usr/src`（提供内核头文件支持动态 eBPF 程序编译——该依赖项[可能在后续版本中移除][1]）

以下是单节点最小化配置示例：

```yaml
$ cat - > ./local-cluster-config.yaml << EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: my-cluster
nodes:
- role: control-plane
  image: kindest/node:v1.27.3@sha256:3966ac761ae0136263ffdb6cfd4db23ef8a83cba8a463690e98317add2c9ba72
  extraMounts:
  - hostPath: /proc
    containerPath: /proc-host
  - hostPath: /usr/src
    containerPath: /usr/src
EOF
```

可通过以下任一方式启动集群：

```console
export CLUSTER_NAME="my-cluster"  # 可使用 --name 标志覆盖配置中的集群名称
kind create cluster --name=$CLUSTER_NAME --config=./local-cluster-config.yaml
```

或直接执行：

```console
make cluster-up
```

注意：`kind` 会自动将当前 `kubeconfig` 上下文切换至新创建的集群。

[1]: https://github.com/sustainable-computing-io/kepler/issues/716

（说明：译文严格保留原文技术术语和代码格式，对长句进行了符合中文阅读习惯的拆分，确保技术文档的准确性和可读性。特殊名词"Kepler"、"eBPF"等保持原状，YAML配置块和命令行示例完整保留原始格式）