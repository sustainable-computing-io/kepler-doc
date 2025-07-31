# 本地集群设置

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

Kepler 运行在 Kubernetes 上。如果您已经有权访问集群，可以跳过此部分。要部署本地集群，
您可以使用 [kind](https://kind.sigs.k8s.io/)。`kind` 是一个使用 Docker 容器
"节点"运行本地 Kubernetes 集群的工具。它主要是为测试 Kubernetes 本身而设计的，
但也可用于本地开发或 CI。

## 安装 Kind

要安装 `kind`，请[参见此处的说明](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)。

我们需要配置集群以运行 Kepler。具体来说，我们需要将 `/proc`（以公开有关在主机上
运行的进程的信息）和 `/usr/src`（以公开允许动态 eBPF 程序编译的内核头文件 -
此依赖项[可能在未来版本中移除][1]）挂载到节点容器中。以下是最小的单节点示例配置：

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

然后我们可以通过以下方式启动集群：

```console
export CLUSTER_NAME="my-cluster"  # 我们可以使用 --name 标志覆盖配置中的名称
kind create cluster --name=$CLUSTER_NAME --config=./local-cluster-config.yaml
```

或者简单地运行：

```console
make cluster-up
```

请注意，`kind` 会自动将您当前的 `kubeconfig` 上下文切换到新创建的集群。

[1]: https://github.com/sustainable-computing-io/kepler/issues/716
