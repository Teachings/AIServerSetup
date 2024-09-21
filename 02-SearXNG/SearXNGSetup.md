# Running SearXNG with Custom Settings in Docker

## Overview

This guide walks you through the steps to run a SearXNG instance in Docker using a custom `settings.yml` configuration file. This setup is ideal for users who want to customize their SearXNG instance without needing to rebuild the Docker image every time they make a change.

## Prerequisites

- **Docker**: Ensure Docker is installed on your machine. Verify the installation by running `docker --version`.
- **Git**: For cloning the SearXNG repository, make sure Git is installed.

## Steps

### 1. Use the Official Image or Clone the SearXNG Repository

You can pull the official image directly from Docker Hub:

```bash
docker pull docker.io/searxng/searxng:latest
```

### 2. Customize `settings.yml`

Place your custom `settings.yml` file in the directory of your choice. Ensure that this file is configured according to your needs, including enabling JSON responses if required.

### 3. Run the SearXNG Docker Container

Run the Docker container using your custom `settings.yml` file. Choose the appropriate command based on whether you are using the official image or a custom build.

#### For the Official Image:

```bash
docker run -d -p 4000:8080 --restart always --name searxng -v ./settings.yml:/etc/searxng/settings.yml searxng/searxng:latest
```

#### Command Breakdown:
- `-d`: Runs the container in detached mode.
- `-p 4000:8080`: Maps port 8080 in the container to port 4000 on your host machine.
- `-v ./settings.yml:/etc/searxng/settings.yml`: Mounts the custom `settings.yml` file into the container.
- `searxng/searxng:latest` or `searxng/searxng`: The Docker image being used.

### 4. Access SearXNG

Once the container is running, you can access your SearXNG instance by navigating to `http://<hostname>:4000` in your web browser.

### 5. Testing JSON Output

To verify that the JSON output is correctly configured, you can use `curl` or a similar tool:

```bash
curl http://<hostname>:4000/search?q=python&format=json
```

This should return search results in JSON format.

### 5. Configuration URL for OpenWebUI

http://<hostname>:4000/search?q=<query>