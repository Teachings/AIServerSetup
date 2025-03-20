### Wiki: Updating Docker Containers for Ollama and OpenWebUI

This guide explains the steps to update Docker containers for **Ollama** and **OpenWebUI**. Follow the instructions below to stop, remove, pull new images, and run the updated containers.

---

## Ollama

### Steps to Update

1. **Stop Existing Containers**
2. **Remove Existing Containers**
3. **Pull the Latest Ollama Image**
4. **Run Updated Containers**
 
For GPU devices 0 and 1:

```bash
docker stop ollama
docker rm ollama
docker pull ollama/ollama
docker run -d --gpus '"device=0,1"' -v ollama:/root/.ollama -p 11434:11434 --restart always --name ollama -e OLLAMA_KEEP_ALIVE=1h ollama/ollama
```

For NVIDIA jetson/cpu

```bash
docker stop ollama
docker rm ollama
docker pull ollama/ollama
docker run -d -v ollama:/root/.ollama -p 11434:11434 --restart always --name ollama -e OLLAMA_KEEP_ALIVE=1h ollama/ollama
```
---

## OpenWebUI

```bash
docker stop open-webui
docker rm open-webui
docker pull ghcr.io/open-webui/open-webui:main
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

---

### Notes
- Make sure to adjust GPU allocation or port numbers as necessary for your setup.
- The `OLLAMA_KEEP_ALIVE` environment variable is set to `1h` to maintain the container alive for an hour after inactivity.
