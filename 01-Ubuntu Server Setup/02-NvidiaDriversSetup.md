## How to Install the Latest Version of NVIDIA CUDA on Ubuntu 22.04 LTS

If you’re looking to unlock the power of your NVIDIA GPU for scientific computing, machine learning, or other parallel workloads, CUDA is essential. Follow this step-by-step guide to install the latest CUDA release on Ubuntu 22.04 LTS.

### Prerequisites

Before proceeding with installing CUDA, ensure your system meets the following requirements:

- **Ubuntu 22.04 LTS** – This version is highly recommended for stability and compatibility.
- **NVIDIA GPU + Drivers** – CUDA requires having an NVIDIA GPU along with proprietary Nvidia drivers installed.

To check for an NVIDIA GPU, open a terminal and run:
```bash
lspci | grep -i NVIDIA
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

1. Visit NVIDIA’s CUDA Download Page and select "Linux", "x86_64", "Ubuntu", "22.04", "deb(network)"
2. Copy the repository installation commands for Ubuntu 22.04:
```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
```
Run these commands to download repository metadata and add the apt source.

### Step 3: Install CUDA Toolkit

Install CUDA using apt:
```bash
sudo apt-get -y install cuda
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

### OPTIONAL: Setting Up cuDNN with CUDA: A Comprehensive Guide

This guide will walk you through downloading cuDNN from NVIDIA's official site, extracting it, copying the necessary files to the CUDA directory, and setting up environment variables for CUDA.

#### Step 1: Download cuDNN

1. **Visit the NVIDIA cuDNN Archive**: 
   Navigate to the [NVIDIA cuDNN Archive](https://developer.nvidia.com/rdp/cudnn-archive).

2. **Select the Version**: 
   Choose the appropriate version of cuDNN compatible with your CUDA version. For this guide, we'll assume you are downloading `cudnn-linux-x86_64-8.9.7.29_cuda12-archive`.

3. **Download the Archive**: 
   Download the `tar.xz` file to your local machine.

#### Step 2: Extract cuDNN

1. **Navigate to the Download Directory**: 
   Open a terminal and navigate to the directory where the archive was downloaded.

   ```bash
   cd ~/Downloads
   ```

2. **Extract the Archive**: 
   Use the `tar` command to extract the contents of the archive.

   ```bash
   tar -xvf cudnn-linux-x86_64-8.9.7.29_cuda12-archive.tar.xz
   ```

   This will create a directory named `cudnn-linux-x86_64-8.9.7.29_cuda12-archive`.

#### Step 3: Copy cuDNN Files to CUDA Directory

1. **Navigate to the Extracted Directory**: 
   Move into the directory containing the extracted cuDNN files.

   ```bash
   cd cudnn-linux-x86_64-8.9.7.29_cuda12-archive
   ```

2. **Copy Header Files**: 
   Copy the header files to the CUDA include directory.

   ```bash
   sudo cp include/cudnn*.h /usr/local/cuda-12.5/include/
   ```

3. **Copy Library Files**: 
   Copy the library files to the CUDA lib64 directory.

   ```bash
   sudo cp lib/libcudnn* /usr/local/cuda-12.5/lib64/
   ```

4. **Set Correct Permissions**: 
   Ensure the copied files have the appropriate permissions.

   ```bash
   sudo chmod a+r /usr/local/cuda-12.5/include/cudnn*.h /usr/local/cuda-12.5/lib64/libcudnn*
   ```

#### Step 4: Set Up Environment Variables

1. **Open Your Shell Profile**: 
   Open your `.bashrc` or `.bash_profile` file in a text editor.

   ```bash
   nano ~/.bashrc
   ```

2. **Add CUDA to PATH and LD_LIBRARY_PATH**: 
   Add the following lines to set the environment variables for CUDA. This example assumes CUDA 12.5.

   ```bash
   export PATH=/usr/local/cuda-12.5/bin:$PATH
   export LD_LIBRARY_PATH=/usr/local/cuda-12.5/lib64:$LD_LIBRARY_PATH
   ```

3. **Apply the Changes**: 
   Source the file to apply the changes immediately.

   ```bash
   source ~/.bashrc
   ```

#### Verification

1. **Check CUDA Installation**: 
   Verify that CUDA is correctly set up by running:

   ```bash
   nvcc --version
   ```

2. **Check cuDNN Installation**: 
   Optionally, you can compile and run a sample program to ensure cuDNN is working correctly.

By following these steps, you will have downloaded and installed cuDNN, integrated it into your CUDA setup, and configured your environment variables for smooth operation. This ensures that applications requiring both CUDA and cuDNN can run without issues.