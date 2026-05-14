# RTX PRO 6000 Blackwell Server Configuration

## Current Hardware Configuration

**Server Specs:**
- **OS:** Ubuntu 24.04.4 LTS (Noble Numbat)
- **Driver:** 595.45.04 (NVIDIA Open Kernel Module)
- **CUDA:** 13.2

**GPU Configuration:**

| Index | GPU Model | PCIe Bus ID | Memory | Current Power Limit | Default Power Limit | Min | Max |
|-------|----------|------------|--------|-------------------|-------------------|-----|-----|
| 0 | NVIDIA RTX PRO 6000 Blackwell | 00000000:16:00.0 | 98,787 MiB | **400W** | 600W | 150W | 600W |
| 1 | NVIDIA GeForce RTX 5060 Ti | 00000000:90:00.0 | 16,311 MiB | **150W** | 180W | 150W | 206W |
| 2 | NVIDIA RTX PRO 6000 Blackwell | 00000000:AC:00.0 | 98,787 MiB | **400W** | 600W | 150W | 600W |

## GPU Details

### RTX PRO 6000 Blackwell (Slots 0 & 2)
- **Architecture:** Blackwell (GB200)
- **VBIOS:** 98.02.81.00.07
- **Board Part:** 900-5G144-2200-000
- **Performance State:** P1 (under load)
- **PCIe:** Gen 5 x16
- **Clocks:** SM 2865 MHz / Memory 13365 MHz (under load)
- **Current Temp:** 56°C / 49°C

### RTX 5060 Ti (Slot 1)
- **Architecture:** Blackwell (GB206)
- **PCIe:** Gen 5
- **Clocks:** SM 262 MHz / Memory 405 MHz (idle)
- **Current Temp:** 29°C
- **Status:** Idle (used for display or standby)

## Current Power Limit Service

Power limits are managed via systemd service. Check current limits:

```bash
nvidia-smi -q -d POWER
```

### Service File: Create If Not Present
```
/etc/systemd/system/nvidia-power-limit.service
```

**Note:** The service file was not found on the server. Run the commands below to create it.

#### Create the Service

```bash
sudo nano /etc/systemd/system/nvidia-power-limit.service
```

Add the following content:

```ini
[Unit]
Description=Set NVIDIA GPU Power Limit

[Service]
Type=oneshot
ExecStart=/usr/bin/nvidia-smi -i 0 -pl 400
ExecStart=/usr/bin/nvidia-smi -i 1 -pl 150
ExecStart=/usr/bin/nvidia-smi -i 2 -pl 400

[Install]
WantedBy=multi-user.target
```

### Managing the Service

```bash
# Reload after changes
sudo systemctl daemon-reload

# Apply immediately
sudo systemctl start nvidia-power-limit.service

# Enable on boot
sudo systemctl enable nvidia-power-limit.service

# Check status
sudo systemctl status nvidia-power-limit.service

# Verify power limits
nvidia-smi --query-gpu=index,name,power.limit,power.draw --format=csv
```

## Quick GPU Status Check

```bash
# All GPUs summary
nvidia-smi

# Power limits
nvidia-smi --query-gpu=index,name,power.limit,power.draw,temperature.gpu,utilization.gpu --format=csv

# Memory usage
nvidia-smi --query-gpu=index,memory.used,memory.total --format=csv

# Clock speeds
nvidia-smi --query-gpu=index,clocks.current.sm,clocks.current.memory --format=csv
```
