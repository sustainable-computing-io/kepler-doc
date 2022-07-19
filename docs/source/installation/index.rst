============
Installation
============

Prerequiste
-----------

- `go <https://go.dev/doc/install>`_
  
- `crio <https://cri-o.io/>`_ & `crictl <https://github.com/kubernetes-sigs/cri-tools/blob/master/docs/crictl.md#install-crictl>`_
 
.. code-block:: bash
 
    sudo dnf module list cri-o
    VERSION=1.21
    sudo dnf module enable cri-o:$VERSION
    sudo dnf install -y crio
    sudo systemctl enable cri-o --now

- podman

- Kubernetes  Any Kubernetes environment will work. For e.g. MicroShift. Refer `microshift <https://microshift.io/docs/getting-started/#deploying-microshift>`_ for installation


kube-prometheus
---------------
.. code-block:: bash
    
    git clone https://github.com/prometheus-operator/kube-prometheus
    kubectl apply --server-side -f manifests/setup
    until kubectl get servicemonitors --all-namespaces ; do date; sleep 1; echo ""; done
    kubectl apply -f manifests/

Kepler
------
.. code-block:: bash

    git clone https://github.com/sustainable-computing-io/kepler.git
    cd kepler

    sudo dnf update -y &&
    sudo dnf install -y bcc-devel.x86_64

    kubectl apply -f manifests/kubernetes/deployment.yaml 
    kubectl apply -f manifests/kubernetes/keplerExporter-serviceMonitor.yaml



