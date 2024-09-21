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