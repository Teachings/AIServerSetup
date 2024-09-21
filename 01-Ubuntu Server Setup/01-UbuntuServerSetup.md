## How to Install the Latest Version of NVIDIA CUDA on Ubuntu 22.04 LTS

If you’re looking to unlock the power of your NVIDIA GPU for scientific computing, machine learning, or other parallel workloads, CUDA is essential. Follow this step-by-step guide to install the latest CUDA release on Ubuntu 22.04 LTS.

### Prerequisites

Before proceeding with installing CUDA, ensure your system meets the following requirements:

- **Ubuntu 22.04 LTS** – This version is highly recommended for stability and compatibility.
- **NVIDIA GPU + Drivers** – CUDA requires having an NVIDIA GPU along with proprietary Nvidia drivers installed.

To check for an NVIDIA GPU, open a terminal and run:
```bash
lspci | grep -i nvidia
```
If an NVIDIA GPU is present, it will be listed. If not, consult NVIDIA’s documentation on installing the latest display drivers.

### Step 1: Install Latest NVIDIA Drivers

Install the latest NVIDIA drivers matched to your GPU model and CUDA version using Ubuntu’s built-in Additional Drivers utility:

1. Open **Settings -> Software & Updates -> Additional Drivers**
2. Select the recommended driver under the NVIDIA heading
3. Click **Apply Changes** and **Reboot**

Verify the driver installation by running:
```bash
nvidia-smi
```
This should print details on your NVIDIA GPU and driver version.

### Step 2: Add the CUDA Repository

Add NVIDIA’s official repository to your system to install CUDA:

1. Visit NVIDIA’s CUDA Download Page and select "Linux", "x86_64", "Ubuntu", "22.04", "deb(local)"
2. Copy the repository installation commands for Ubuntu 22.04:
```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600  
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/ /"  
sudo apt-get update
```
Run these commands to download repository metadata and add the apt source.

### Step 3: Install CUDA Toolkit

Install CUDA using apt:
```bash
sudo apt-get install cuda
```
Press **Y** to proceed and allow the latest supported version of the CUDA toolkit to install.

### Step 4: Configure Environment Variables

Update environment variables to recognize the CUDA compiler, tools, and libraries:

Open `/etc/profile.d/cuda.sh` and add the following configuration:
```bash
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
```
Save changes and refresh environment variables:
```bash
source /etc/profile.d/cuda.sh
```
Alternatively, reboot to load the updated environment variables.

### Step 5: Verify Installation

Validate the installation:

1. Check the `nvcc` compiler version:
   ```bash
   nvcc --version
   ```
   This should display details on the CUDA compile driver, including the installed version.

2. Verify GPU details with NVIDIA SMI:
   ```bash
   nvidia-smi
   ```

You can now leverage the power of your GPU for parallel workloads.