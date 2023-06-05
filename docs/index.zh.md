# Kubernetes Efficient Power Level Exporter (Kepler)

Kepler (Kubernetes-based Efficient Power Level Exporter)是一个prometheus exportor。
它通过eBPF技术与CPU性能计数器以及Linux内核的tracepoints进行交互。

这些数据和来自cgroup或者sysfs的信息一起可以放入机器学习模型中来对pod的能耗进行预测。


项目的Github地址 ➡️ [Kepler](https://github.com/sustainable-computing-io/kepler).
目前中文文档依旧在施工中，欢迎贡献。

</br></br></br></br></br></br></br></br>
<p style="text-align: center;">
目前该项目已经成为Cloud Native Computing Foundation sandbox project.

<img src="cncf-color-bg.svg" width="40%" height="20%">
</p>