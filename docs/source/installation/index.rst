============
Installation
============

Prerequiste
-----------

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


    kubectl apply -f manifests/kubernetes/deployment.yaml 
    kubectl apply -f manifests/kubernetes/keplerExporter-serviceMonitor.yaml



