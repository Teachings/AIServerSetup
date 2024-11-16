# **PORT Forward Trick with Bolt.new: Setup and Installation Guide**

This guide showcases the port forward trick for apps that do not allow customization. I take an example of `bolt.new-any-llm` repo for this usecase. 

It walks you through the installation and setup of `bolt.new-any-llm`. If you encounter any installation issues, submit an [issue](https://github.com/coleam00/bolt.new-any-llm/issues) or fork and improve this documentation through a pull request.

---

## **Prerequisites**

### 1. Install Git
Download and install Git from [https://git-scm.com/downloads](https://git-scm.com/downloads).

### 2. Install Node.js
Download and install Node.js from [https://nodejs.org/en/download/](https://nodejs.org/en/download/).

### 3. Verify Node.js in Your Path
Ensure the Node.js installation is in your system path:

- **Windows**: Search for "Edit the system environment variables," select "Environment Variables," and ensure the `Path` variable includes Node.js.
- **Mac/Linux**: Open Terminal and run:
  ```bash
  echo $PATH
  ```
  Check that `/usr/local/bin` is in the output.

---

## **Clone the Repository**

1. Open Terminal (or CMD with admin permissions on Windows).
2. Clone the repository:
   ```bash
   git clone https://github.com/coleam00/bolt.new-any-llm.git
   ```

---

## **Configure Environment Variables**

Rename `.env.example` to `.env.local` and add your LLM API keys. For example:
- On Mac: `~/bolt.new-any-llm/.env.example`
- On Windows/Linux: The path will be similar.

---

## **Set Up the Ollama Service**

### 1. Stop and Disable the Local Ollama Service
If you have Ollama installed locally and running, you need to stop and disable it to avoid conflicts with the remote server:

- **Stop the service**:
  ```bash
  sudo systemctl stop ollama.service
  ```
- **Disable it from restarting**:
  ```bash
  sudo systemctl disable ollama.service
  ```

---

### 2. Forward `localhost` Traffic to the Remote Ollama Server
To route all traffic from `localhost:11434` to your remote server (`ai.mtcl.lan:11434`):

1. Open a terminal and run:
   ```bash
   ssh -L 11434:ai.mtcl.lan:11434 mukul@ai.mtcl.lan
   ```
2. Keep this terminal session running while using the application.

---

### 3. Extend Ollama Model Context Length

Ollama models by default have a context length of 2048 tokens. To increase this for a specific model (`qwen2.5-coder:32b`), follow these steps:

1. SSH into your remote server:
   ```bash
   ssh mukul@ai.mtcl.lan
   ```
2. Access the Docker container running Ollama:
   ```bash
   docker exec -it ollama1 /bin/bash
   ```
3. Create a `Modelfile` with the following content:
   ```bash
   echo "FROM qwen2.5-coder:32b" > /tmp/Modelfile
   echo "PARAMETER num_ctx 32768" >> /tmp/Modelfile
   ```
4. Create the new model with an extended context:
   ```bash
   ollama create -f /tmp/Modelfile qwen2.5-coder-extra-ctx:32b
   ```
5. Verify the new model:
   ```bash
   ollama list
   ```
   You should see `qwen2.5-coder-extra-ctx:32b` in the list.

6. Exit the Docker container:
   ```bash
   exit
   ```

---

## **Run the Application Without Docker**

1. **Install Dependencies**
   Navigate to the cloned repository directory and run:
   ```bash
   pnpm install
   ```

2. **Start the Application**
   Start the development server:
   ```bash
   pnpm run dev
   ```

---

## **Summary**
This guide ensures that your local environment routes traffic seamlessly to the remote Ollama server, extends the context length for large models, and sets up the `bolt.new-any-llm` repository for local development. If you face issues, consult the repository's [issue tracker](https://github.com/coleam00/bolt.new-any-llm/issues). 
