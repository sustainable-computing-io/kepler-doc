## Steps to solve kepler/prometheus configuration issues during deployment via helm in K8S cluster
- issue: prometheus can not discover kepler under its service montior. Tryt the below steps to resolve it.

- Deploy Prometheus using Prometheus operator https://sustainable-computing.io/installation/kepler/#deploy-the-prometheus-operator 
It is better to use the same name space for kepler and Prometheus to avoid access control issues.

- changes to be done in the values.yaml  https://github.com/sustainable-computing-io/kepler-helm-chart/blob/main/chart/kepler/values.yaml <br>
  <br>
  serviceMonitor: <br>
  &ensp;enabled: true <br>
  &ensp;namespace: "name of the namespace" <br>
  &ensp;interval: 30s <br>
  &ensp;scrapeTimeout: 20s <br>
  &ensp;labels: {} <br>

### if you use different namespace for Prometheus and Kepler then deploy also <br> <br>
 - Prometheus role (modify system namespace to Kepler namespace): https://github.com/sustainable-computing-io/kepler/blob/main/manifests/config/rbac/prometheus_role.yaml <br>
 - Prometheus role-binding (modify Kepler and Prometheus namespace): https://github.com/sustainable-computing-io/kepler/blob/main/manifests/config/rbac/prometheus_role_binding.yaml <br>


