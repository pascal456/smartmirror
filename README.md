# smartmirror Overview

# configuration instructions

## pigpio library
pigpio is one possibility to control the GPIOs of the Raspberry PI.

### installation

to control the LED strip, `pigpio` needs to be installed

```console
sudo apt-get install pigpio
```

to install the python library
```console
pip install pigpio
```

### start and stop the deamon

to be controlled via e.g. python code, the deamon needs to be started
```console
sudo systemctl start pigpiod
```

to stop it again:
```console
sudo systemctl stop pigpiod
```

to see the **statup status**:
```console
sudo systemctl status pigpiod
```

to **automatically** start the deamon on system / raspberry pi startup:
```console
sudo systemctl enable pigpiod
```

to disable again:
```console
sudo systemctl disable pigpiod
```