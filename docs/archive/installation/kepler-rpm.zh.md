# 将 Kepler 安装为 RPM

!!! warning "机器翻译声明"
    本文档由 AI 语言模型 (Claude) 从英文自动翻译而成。如发现翻译错误或不准确之处，请在 [Kepler 文档项目](https://github.com/sustainable-computing-io/kepler-doc/issues) 中提交 issue 报告问题。

## 版本 0.7.10 及更新版本
当前的 rpm 发行版是一个启动 podman 容器的 systemd 单元。

从 Kepler 发布 URL [下载](https://github.com/sustainable-computing-io/kepler/releases/)
最新稳定版本

```sh
tar xvzf kepler.rpm.tar.gz
yum install RPMS/noarch/container-kepler-0.7.10-1.noarch.rpm
systemctl enable container-kepler --now
```

通过以下命令验证 podman 启动了 kepler 容器：

`sudo podman ps`

然后通过浏览器访问预配置端口上的以下 URL [浏览器](http://localhost:8888/metrics)

或通过 curl 命令：

`curl localhost:8888/metrics | grep kepler_node_package_joules_total`


## 0.7.10 之前的版本
较旧版本直接将 kepler 安装为 rpm 包（而不是像新版本中那样作为容器）
要安装 Kepler RPM [下载](https://github.com/sustainable-computing-io/kepler/releases/)
最新稳定版本，解压并安装：

```sh
sudo dnf localinstall kepler-[version.arch].rpm

systemctl start kepler.service
```

检查状态：

```sh
systemctl status kepler.service

journalctl -f | grep kepler
```

为了启用进程级能量统计，请输入：

```sh
mkdir -p /etc/kepler/kepler.config
echo -n true > /etc/kepler/kepler.config/ENABLE_PROCESS_METRICS
```

kepler 服务在默认端口 8888 上运行。

使用您的网络浏览器导航到机器 IP 的端口 8888。
