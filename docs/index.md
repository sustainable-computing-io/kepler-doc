# Kubernetes Efficient Power Level Exporter (Kepler)

Kepler (Kubernetes-based Efficient Power Level Exporter) is a Prometheus exporter that measures energy consumption at the container, pod, VM, and process level by reading hardware sensors and attributing power based on resource utilization.

Kepler uses Intel RAPL (Running Average Power Limit) sensors to collect energy data from CPU packages, cores, and memory subsystems, then distributes this energy proportionally to workloads based on their CPU time consumption.

Check out the project on GitHub ➡️ [Kepler](https://github.com/sustainable-computing-io/kepler).

For a comprehensive overview, please check out ➡️ [this CNCF blog article](https://www.cncf.io/blog/2023/10/11/exploring-keplers-potentials-unveiling-cloud-application-power-consumption/).

<!-- markdownlint-disable -->
</br></br></br></br></br></br></br></br>
<p style="text-align: center;">
We are a Cloud Native Computing Foundation sandbox project.
</br>
<img src="cncf-color-bg.svg" width="40%" height="20%">
</p>
<!-- markdownlint-enable -->
