# Deploy using Manifests

## Getting Started

Before you deploy kepler make sure:

- you have a Kubernetes cluster running. If you want to do local cluster set up [follow this](./local-cluster.md#install-kind) 
- the Monitoring stack, i.e. Prometheus with Grafana is set up. [Steps here](#deploy-the-prometheus-operator)

>The default Grafana deployment can be accessed with the credentials `admin:admin`. You can expose the web-based UI locally using: 

```sh
kubectl -n monitoring port-forward svc/grafana 3000
```


#### Running Kepler on a local kind cluster

To run Kepler on `kind`, we need to build it locally with specific flags. The full details of local builds are covered in the [section below](#build-manifests). To deploy on a local `kind` cluster, you need to use the `CI_DEPLOY` and `PROMETHEUS_DEPLOY` flags.

```sh
git clone --depth 1 git@github.com:sustainable-computing-io/kepler.git
cd ./kepler
make build-manifest OPTS="CI_DEPLOY PROMETHEUS_DEPLOY"
kubectl apply -f _output/generated-manifest/deployment.yaml
```

The following deployment will also create a service listening on port `9102`.

>If you followed the Kepler dashboard deployment steps, you can access the Kepler dashboard by navigating to [http://localhost:3000/](http://localhost:3000/) Login using `admin:admin`. Skip the window where Grafana asks to input a new password.


![](../fig/grafana_dashboard.png)


#### Build manifests
First, fork the [kepler](https://github.com/sustainable-computing-io/kepler) repository and clone it.

If you want to use Redfish BMC and IPMI, you need to add Redfish and IPMI credentials of each of the kubelet node to the `redfish.csv` under the `kepler/manifests/config/exporter` directory. The format of the file is as follows:

```csv
kubelet_node_name_1,redfish_username_1,redfish_password_2,https://redfish_ip_or_hostname_1
kubelet_node_name_2,redfish_username_2,redfish_password_2,https://redfish_ip_or_hostname_2
```

where, `kubelet_node_name` in the first column is the name of the node where the kubelet is running. You can get the name of the node by running the following command:

```bash
kubectl get nodes
```

`redfish_username` and `redfish_password` in the second and third columns are the credentials to access the Redfish API from each node. 
While `https://redfish_ip_or_hostname` in the fourth column is the Redfish endpoint in IP address or hostname.


Then, build the manifests file that suit your environment and deploy it with the following steps:

```bash
make build-manifest OPTS="<deployment options>"
# minimum deployment: 
# > make build-manifest
# deployment with sidecar on openshift: 
# > make build-manifest OPTS="ESTIMATOR_SIDECAR_DEPLOY OPENSHIFT_DEPLOY"
```
Manifests will be generated in  `_output/manifests/kubernetes/generated/` by default.

Deployment Option|Description|Dependency
---|---|---
BM_DEPLOY|baremetal deployment patched with node selector feature.node.kubernetes.io/cpu-cpuid.HYPERVISOR to not exist|-
OPENSHIFT_DEPLOY|patch openshift-specific attribute to kepler daemonset and deploy SecurityContextConstraints|-
PROMETHEUS_DEPLOY|patch prometheus-related resource (ServiceMonitor, RBAC role, rolebinding) |require prometheus deployment which can be OpenShift integrated or [custom deploy](#deploy-the-prometheus-operator)
CLUSTER_PREREQ_DEPLOY|deploy prerequisites for kepler on openshift cluster| OPENSHIFT_DEPLOY option set
CI_DEPLOY|update proc path for kind cluster using in CI|-
ESTIMATOR_SIDECAR_DEPLOY|patch estimator sidecar and corresponding configmap to kepler daemonset|-
MODEL_SERVER_DEPLOY|deploy model server and corresponding configmap to kepler daemonset|-
TRAIN_DEPLOY|patch online-trainer sidecar to model server| MODEL_SERVER_DEPLOY option set

Following options are available for Redfish client, you can set them as environment variables of kepler-exporter. They affect all of Redfish access from Kepler Exporter.

Option|Default value|Description
---|---
REDFISH_PROBE_INTERVAL_IN_SECONDS|60|Interval in seconds to get power consumption via Redfish.
REDFISH_SKIP_SSL_VERIFY|true|`true` if TLS verification is disabled on connecting to Redfish endpoint.

`build-manifest` requirements:
-  kubectl v1.21+
-  make
-  go



## Deploy the Prometheus operator

If Prometheus is already installed in the cluster, skip this step. Otherwise, follow these steps to install it.

1. Clone the [kube-prometheus](https://github.com/prometheus-operator/kube-prometheus) project to your local folder, and enter the `kube-prometheus` directory.

```sh
git clone --depth 1 https://github.com/prometheus-operator/kube-prometheus
cd kube-prometheus
```

2. This step is optional. You can later manually add the [Kepler Grafana dashboard](https://raw.githubusercontent.com/sustainable-computing-io/kepler/main/grafana-dashboards/Kepler-Exporter.json) through the Grafana UI. To automatically do that, fetch the `kepler-exporter` Grafana dashboard and inject in the Prometheus Grafana deployment. This step uses [yq](https://github.com/mikefarah/yq), a YAML processor:

```sh
KEPLER_EXPORTER_GRAFANA_DASHBOARD_JSON=`curl -fsSL https://raw.githubusercontent.com/sustainable-computing-io/kepler/main/grafana-dashboards/Kepler-Exporter.json | sed '1 ! s/^/         /'`
mkdir -p grafana-dashboards
cat > ./grafana-dashboards/kepler-exporter-configmap.yaml<<-EOF
apiVersion: v1
data:
    kepler-exporter.json: |-
        $KEPLER_EXPORTER_GRAFANA_DASHBOARD_JSON
kind: ConfigMap
metadata:
    labels:
        app.kubernetes.io/component: grafana
        app.kubernetes.io/name: grafana
        app.kubernetes.io/part-of: kube-prometheus
        app.kubernetes.io/version: 9.5.3
    name: grafana-dashboard-kepler-exporter
    namespace: monitoring
EOF
yq -i e '.items += [load("./grafana-dashboards/kepler-exporter-configmap.yaml")]' ./manifests/grafana-dashboardDefinitions.yaml
yq -i e '.spec.template.spec.containers.0.volumeMounts += [ {"mountPath": "/grafana-dashboard-definitions/0/kepler-exporter", "name": "grafana-dashboard-kepler-exporter", "readOnly": false} ]' ./manifests/grafana-deployment.yaml
yq -i e '.spec.template.spec.volumes += [ {"configMap": {"name": "grafana-dashboard-kepler-exporter"}, "name": "grafana-dashboard-kepler-exporter"} ]' ./manifests/grafana-deployment.yaml
```

3. Finally, apply the objects in the `manifests` directory. This will create the `monitoring` namespace and CRDs, and then wait for them to be available before creating the remaining resources. During the `until` loop, a response of `No resources found` is to be expected. This statement checks whether the resource API is created but doesn't expect the resources to be there.

```sh
kubectl apply --server-side -f manifests/setup
until kubectl get servicemonitors --all-namespaces ; do date; sleep 1; echo ""; done
kubectl apply -f manifests/
```
