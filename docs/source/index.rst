.. Kepler documentation master file, created by
   sphinx-quickstart on Tue Jun  7 10:57:32 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========
Overview
========

.. toctree::
   :caption: Contents
   :hidden:
   :titlesonly:
   :includehidden:

   self
   installation/index
   usage/index
   design/index

*Kubernetes Efficient Power Level Exporter*

Kepler (Kubernetes-based Efficient Power Level Exporter) is a Prometheus exporter. It uses eBPF to probe CPU performance counters and Linux kernel tracepoints. These data and stats from cgroup and sysfs are fed into ML models to estimate energy consumption by Pods.

Check us out on GitHub ➡️ https://github.com/sustainable-computing-io/kepler

