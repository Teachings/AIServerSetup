# **Port Forwarding Magic: Set Up Bolt.New with Remote Ollama Server and Qwen2.5-Coder:32B**

This guide demonstrates how to use **port forwarding** to connect your local **Bolt.New** setup to a **remote Ollama server**, solving issues with apps that don’t allow full customization. We’ll use the open-source [Bolt.New repository](https://github.com/coleam00/bolt.new-any-llm) as our example, and we’ll even show you how to extend the context length for the popular **Qwen2.5-Coder:32B model**.

If you encounter installation issues, submit an [issue](https://github.com/coleam00/bolt.new-any-llm/issues) or contribute by forking and improving this guide.

---

## **What You'll Learn**
- Clone and configure **Bolt.New** for your local development.
- Use **SSH tunneling** to seamlessly forward traffic to a remote server.
- Extend the context length of AI models for enhanced capabilities.
- Run **Bolt.New** locally.

---

## **Prerequisites**

Download and install Node.js from [https://nodejs.org/en/download/](https://nodejs.org/en/download/).

---

## **Step 1: Clone the Repository**

1. Open Terminal.
2. Clone the repository:
   ```bash
   git clone https://github.com/coleam00/bolt.new-any-llm.git
   ```

---

## **Step 2: Stop Local Ollama Service**

If Ollama is already running on your machine, stop it to avoid conflicts with the remote server.

- **Stop the service**:
   ```bash
   sudo systemctl stop ollama.service
   ```
- **OPTIONAL: Disable it from restarting**:
   ```bash
   sudo systemctl disable ollama.service
   ```

---

## **Step 3: Forward Local Traffic to the Remote Ollama Server**

To forward all traffic from `localhost:11434` to your remote Ollama server (`ai.mtcl.lan:11434`), set up SSH tunneling:

1. Open a terminal and run:
   ```bash
   ssh -L 11434:ai.mtcl.lan:11434 mukul@ai.mtcl.lan
   ```
   - Replace `mukul` with your remote username.
   - Replace `ai.mtcl.lan` with your server's hostname or IP.

2. Keep this terminal session running while using Bolt.New. This ensures your app communicates with the remote server as if it’s local.

---

## **Step 4: OPTIONAL: Extend Ollama Model Context Length**

By default, Ollama models have a context length of 2048 tokens. For tasks requiring larger input, extend this limit for **Qwen2.5-Coder:32B**:

1. SSH into your remote server:
   ```bash
   ssh mukul@ai.mtcl.lan
   ```
2. Access the Docker container running Ollama:
   ```bash
   docker exec -it ollama /bin/bash
   ```
3. Create a `Modelfile`:

   While inside the Docker container, run the following commands to create the Modelfile:

   ```bash
   echo "FROM qwen2.5-coder:32b" > /tmp/Modelfile
   echo "PARAMETER num_ctx 32768" >> /tmp/Modelfile
   ```
   If you prefer, you can use cat to directly create the file:
   ```bash
   cat > /tmp/Modelfile << EOF
   FROM qwen2.5-coder:32b
   PARAMETER num_ctx 32768
   EOF
   ```


4. Create the new model:
   ```bash
   ollama create -f /tmp/Modelfile qwen2.5-coder-extra-ctx:32b
   ```
5. Verify the new model:
   ```bash
   ollama list
   ```
   You should see `qwen2.5-coder-extra-ctx:32b` listed.

6. Exit the Docker container:
   ```bash
   exit
   ```

---

## **Step 5: Run Bolt.New Without Docker**

1. **Install Dependencies**  
   Navigate to the cloned repository:
   ```bash
   cd bolt.new-any-llm
   pnpm install
   ```

2. **Start the Development Server**  
   Run:
   ```bash
   pnpm run dev
   ```

---

## **Summary**

This guide walks you through setting up **Bolt.New** with a **remote Ollama server**, ensuring seamless communication through SSH tunneling. We’ve also shown you how to extend the context length for **Qwen2.5-Coder:32B**, making it ideal for advanced development tasks.

With this setup:
- You’ll offload heavy computation to your remote server.
- Your local machine remains light and responsive.
- Buggy `localhost` configurations? No problem—SSH tunneling has you covered.

Credits: [Bolt.New repository](https://github.com/coleam00/bolt.new-any-llm). 

Let’s build something amazing! 🚀