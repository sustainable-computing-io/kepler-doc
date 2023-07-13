# Kepler Community Operator on OpenShift

## Install operator from Operator Hub

Before you start make sure you have a OCP 4.13 cluster running.


1. Go to Operator Hub. Search for `Kepler`. Click on `Install` 
![](../fig/ocp_installation/operator_installation_ocp_1.png)

2. Allow the operator to install
![](../fig/ocp_installation/operator_installation_ocp_7.png)

3. Create a Custom Resource for Kepler 
![](../fig/ocp_installation/operator_installation_ocp_2.png)
> Note: The current OCP console may display a JavaScript error (expected to be fixed in 4.13.5), but it doesn't affect the rest of the steps. Fixes are currently available on the 4.13.0-0.nightly-2023-07-08-165124 build of OCP console.


## Installing the Grafana operator

- Get the API Bearer Token by executing the following `oc` command:
```sh
oc whoami --show-token
sha256~RQOIZC73Hc5pabivSp648Hkke5R0dC45D-7u-RLHVYM
```
- Add the token from `step 1` in `hack/dashboard/openshift/03-grafanadatasource-UPDATETHIS.yaml`
![](../fig/ocp_installation/operator_installation_ocp_3.png)

- Deploy the Grafana Operator by running the following command:
```sh
$ hack/dashboard/openshift/deploy-grafana.sh
```

- Access the Garafana Console Route
![](../fig/ocp_installation/operator_installation_ocp_5.png)

- Sign in to the Grafana Dashboard using the credentials `kepler:kepler`.
![](../fig/ocp_installation/operator_installation_ocp_6.png)