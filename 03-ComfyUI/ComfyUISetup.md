
# ComfyUI Docker Setup with GGUF Support and ComfyUI Manager

This guide provides detailed steps to build and run **ComfyUI** with **GGUF support** and **ComfyUI Manager** using Docker. The GGUF format is optimized for quantized models, and ComfyUI Manager is included for easy node management.

## Prerequisites

Before starting, ensure you have the following installed on your system:

- **Docker**
- **NVIDIA GPU with CUDA support** (if using GPU acceleration)
- **Create Directory structure for git repo Models and Checkpoints**

```bash
mkdir -p ~/dev-ai/vison/models/checkpoints
```

### 1. Clone the ComfyUI Repository

First, navigate to `~/dev-ai/vison` directory and clone the ComfyUI repository to your local machine:

```bash
cd ~/dev-ai/vison
```

```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
```

### 2. Create the Dockerfile

Copy the provided `Dockerfile` in the root of your ComfyUI directory. This file contains the necessary configurations for building the Docker container with GGUF support.

### 3. Build the Docker Image

```bash
docker build -t comfyui-gguf:latest .
```

This will create a Docker image named `comfyui-gguf:latest` with both **ComfyUI Manager** and **GGUF support** built in.

### 4. Run the Docker Container

Once the image is built, you can run the Docker container with volume mapping for your models.

```bash
docker run --name comfyui -p 8188:8188 --gpus all \
  -v /home/mukul/dev-ai/vison/models:/app/models \
  -d comfyui-gguf:latest
```

This command maps your local `models` directory to `/app/models` inside the container and exposes ComfyUI on port `8188`.

### 5. Download and Place Checkpoint Models

Download and place your civitai checkpoint models in the `checkpoints` directory inside the container:
https://civitai.com/models/139562/realvisxl-v50

To use GGUF models or other safetensor models, follow the steps below to download them directly into the `checkpoints` directory.

1. **Navigate to the Checkpoints Directory**:
   ```bash
   cd /home/mukul/dev-ai/vison/models/checkpoints
   ```

2. **Download `flux1-schnell-fp8.safetensors`**:
   ```bash
   wget https://huggingface.co/Comfy-Org/flux1-schnell/resolve/main/flux1-schnell-fp8.safetensors?download=true -O flux1-schnell-fp8.safetensors
   ```

3. **Download `flux1-dev-fp8.safetensors`**:
   ```bash
   wget https://huggingface.co/Comfy-Org/flux1-dev/resolve/main/flux1-dev-fp8.safetensors?download=true -O flux1-dev-fp8.safetensors
   ```

These commands will place the corresponding `.safetensors` files into the `checkpoints` directory.

### 6. Access ComfyUI

After starting the container, access the ComfyUI interface in your web browser:

```bash
http://<your-server-ip>:8188
```

Replace `<your-server-ip>` with your server's IP address or use `localhost` if you're running it locally.

### 7. Using GGUF Models

In the ComfyUI interface:
- Use the **UnetLoaderGGUF** node (found in the `bootleg` category) to load GGUF models.
- Ensure your GGUF files are correctly named and placed in the `/app/models/checkpoints` directory for detection by the loader node.

### 8. Managing Nodes with ComfyUI Manager

With **ComfyUI Manager** built into the image:
- **Install** missing nodes as needed when uploading workflows.
- **Enable/Disable** conflicting nodes from the ComfyUI Manager interface.

### 9. Stopping and Restarting the Docker Container

To stop the running container:

```bash
docker stop comfyui
```

To restart the container:

```bash
docker start comfyui
```

### 10. Logs and Troubleshooting

To view the container logs:

```bash
docker logs comfyui
```

This will provide details if anything goes wrong or if you encounter issues with GGUF models or node management.
