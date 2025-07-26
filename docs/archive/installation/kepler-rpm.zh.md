# 以RPM方式安装Kepler

## 0.7.10及更新版本
当前rpm版本是一个systemd单元，用于启动podman容器。

从Kepler发布页面[下载](https://github.com/sustainable-computing-io/kepler/releases/)最新稳定版本

```sh
tar xvzf kepler.rpm.tar.gz
yum install RPMS/noarch/container-kepler-0.7.10-1.noarch.rpm
systemctl enable container-kepler --now
```

通过以下命令验证podman是否启动了kepler容器：

`sudo podman ps`

然后通过浏览器访问预配置端口的URL [浏览器](http://localhost:8888/metrics)

或使用curl命令：

`curl localhost:8888/metrics | grep kepler_node_package_joules_total`


## 0.7.10之前版本
旧版本直接以rpm包形式安装kepler（与新版本的容器安装方式不同）
安装Kepler RPM包需先[下载](https://github.com/sustainable-computing-io/kepler/releases/)最新稳定版本，解压后安装：

```sh
sudo dnf localinstall kepler-[版本.架构].rpm

systemctl start kepler.service
```

使用以下命令检查状态：

```sh
systemctl status kepler.service

journalctl -f | grep kepler
```

如需启用进程级能耗统计，执行：

```sh
mkdir -p /etc/kepler/kepler.config
echo -n true > /etc/kepler/kepler.config/ENABLE_PROCESS_METRICS
```

kepler服务默认运行在8888端口。

通过浏览器访问机器IP的8888端口即可。