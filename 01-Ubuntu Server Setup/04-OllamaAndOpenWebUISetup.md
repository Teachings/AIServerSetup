# Ollama & OpenWebUI Docker Setup

## Ollama with Nvidia GPU

Ollama makes it easy to get up and running with large language models locally.
To run Ollama using an Nvidia GPU, follow these steps:

### Step 1: Install the NVIDIA Container Toolkit

#### Install with Apt

1. **Configure the repository**:

    ```bash
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
        | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
    curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
        | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
        | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    sudo apt-get update
    ```

2. **Install the NVIDIA Container Toolkit packages**:

    ```bash
    sudo apt-get install -y nvidia-container-toolkit
    ```

#### Install with Yum or Dnf

1. **Configure the repository**:

    ```bash
    curl -s -L https://nvidia.github.io/libnvidia-container/stable/rpm/nvidia-container-toolkit.repo \
        | sudo tee /etc/yum.repos.d/nvidia-container-toolkit.repo
    ```

2. **Install the NVIDIA Container Toolkit packages**:

    ```bash
    sudo yum install -y nvidia-container-toolkit
    ```

### Step 2: Configure Docker to Use Nvidia Driver

```bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

### Step 3: Start the Container

```bash
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

## Running Multiple Instances with Specific GPUs

You can run multiple instances of the Ollama server and assign specific GPUs to each instance. In my server, I have 4 Nvidia 3090 GPUs, which I use as described below:

### Ollama Server for GPUs 0 and 1

```bash
docker run -d --gpus '"device=0,1"' -v ollama:/root/.ollama -p 11435:11434 --restart always --name ollama1 --network ollama-network ollama/ollama
```

### Ollama Server for GPUs 2 and 3

```bash
docker run -d --gpus '"device=2,3"' -v ollama:/root/.ollama -p 11436:11434 --restart always --name ollama2 --network ollama-network ollama/ollama
```

## Running Models Locally

Once the container is up and running, you can execute models using:

```bash
docker exec -it ollama ollama run llama3
```

### Try Different Models

Explore more models available in the [Ollama library](https://github.com/ollama/ollama).

## OpenWebUI Installation

To install and run OpenWebUI, use the following command:

```bash
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```