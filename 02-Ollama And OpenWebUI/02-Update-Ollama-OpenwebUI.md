### Wiki: Updating Docker Containers for Ollama and OpenWebUI

This guide explains the steps to update Docker containers for **Ollama** and **OpenWebUI**. Follow the instructions below to stop, remove, pull new images, and run the updated containers.

---

## Ollama

### Steps to Update

1. **Stop Existing Containers**:
   ```bash
   docker stop ollama ollama1 ollama2
   ```

2. **Remove Existing Containers**:
   ```bash
   docker rm ollama ollama1 ollama2
   ```

3. **Pull the Latest Ollama Image**:
   ```bash
   docker pull ollama/ollama
   ```

4. **Run Updated Containers**:
   - For GPU devices 0 and 1:
     ```bash
     docker run -d --gpus '"device=0,1"' -v ollama:/root/.ollama -p 11435:11434 --restart always --name ollama1 -e OLLAMA_KEEP_ALIVE=1h ollama/ollama
     ```
   - For GPU devices 2 and 3:
     ```bash
     docker run -d --gpus '"device=2,3"' -v ollama:/root/.ollama -p 11436:11434 --restart always --name ollama2 -e OLLAMA_KEEP_ALIVE=1h ollama/ollama
     ```
   - For all GPUs (0, 1, 2, and 3):
     ```bash
     docker run -d --gpus '"device=0,1,2,3"' -v ollama:/root/.ollama -p 11434:11434 --restart always --name ollama -e OLLAMA_KEEP_ALIVE=1h ollama/ollama
     ```

---

## OpenWebUI

### Steps to Update

1. **Stop the Existing Container**:
   ```bash
   docker stop open-webui
   ```

2. **Remove the Existing Container**:
   ```bash
   docker rm open-webui
   ```

3. **Pull the Latest OpenWebUI Image**:
   ```bash
   docker pull ghcr.io/open-webui/open-webui:main
   ```

4. **Run the Updated Container**:
   ```bash
   docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
   ```

---

### Notes
- Make sure to adjust GPU allocation or port numbers as necessary for your setup.
- The `OLLAMA_KEEP_ALIVE` environment variable is set to `1h` to maintain the container alive for an hour after inactivity.
