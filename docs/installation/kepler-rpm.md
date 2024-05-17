# Install Kepler as RPM

## Versions 0.7.10 and newer
The current rpm release is a systemd unit that starts a podman container.

Download the latest stable release from the Kepler release URL [download](https://github.com/sustainable-computing-io/kepler/releases/)

```sh
tar xvzf kepler.rpm.tar.gz
yum install RPMS/noarch/container-kepler-0.7.10-1.noarch.rpm
systemctl enable container-kepler --now
```

Verify that podman starts a kepler container via

`sudo podman ps`

then via your browser pointing to the URL below on the preconfigured port [browser] http://localhost:8888/metrics

or via a curl command:

`curl localhost:8888/metrics | grep kepler_node_package_joules_total`


## Versions prior to 0.7.10
Older version directly install kepler as a rpm package (as opposed to as a container in newer versions)
To install the Kepler RPM [download](https://github.com/sustainable-computing-io/kepler/releases/) the latest stable version, unpack and install:

```sh
sudo dnf localinstall kepler-[version.arch].rpm

systemctl start kepler.service
```

Check status with

```sh
systemctl status kepler.service

journalctl -f | grep kepler
```

In order to do process-level energy accounting type:

```sh
mkdir -p /etc/kepler/kepler.config
echo -n true > /etc/kepler/kepler.config/ENABLE_PROCESS_METRICS
```

The kepler service runs on default port 8888.

Use your web browser to navigate to the machine IP on port 8888.
