# Setting NVIDIA GPU Power Limit at System Startup

## Overview

This guide explains how to set the power limit for NVIDIA GPUs at system startup using a systemd service. This ensures the power limit setting is persistent across reboots.

## Steps

### 1. Create and Configure the Service File

1. Open a terminal and create a new systemd service file:

    ```bash
    sudo nano /etc/systemd/system/nvidia-power-limit.service
    ```

2. Add the following content to the file, replacing `270` with the desired power limit (e.g., 270 watts for your GPUs):

    ```ini
    [Unit]
    Description=Set NVIDIA GPU Power Limit

    [Service]
    Type=oneshot
    ExecStart=/usr/bin/nvidia-smi -i 0 -pl 270
    ExecStart=/usr/bin/nvidia-smi -i 1 -pl 270
    ExecStart=/usr/bin/nvidia-smi -i 2 -pl 270
    ExecStart=/usr/bin/nvidia-smi -i 3 -pl 270

    [Install]
    WantedBy=multi-user.target
    ```

    Save and close the file.

### 2. Apply and Enable the Service

1. Reload the systemd manager configuration:

    ```bash
    sudo systemctl daemon-reload
    ```

2. Enable the service to ensure it runs at startup:

    ```bash
    sudo systemctl enable nvidia-power-limit.service
    ```

### 3. (Optional) Start the Service Immediately

To apply the power limit immediately without rebooting:

```bash
sudo systemctl start nvidia-power-limit.service
```

## Verification

Check the power limits using `nvidia-smi`:

```bash
nvidia-smi -q -d POWER
```

Look for the "Power Management" section to verify the new power limits.

By following this guide, you can ensure that your NVIDIA GPUs have a power limit set at every system startup, providing consistent and controlled power usage for your GPUs.