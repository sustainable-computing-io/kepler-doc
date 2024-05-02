# Install Kepler as RPM

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
