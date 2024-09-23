# Installing Webmin and Docker on Ubuntu

This guide walks you through installing Webmin on Ubuntu and expanding logical volumes via Webmin’s interface. Additionally, it covers Docker installation on Ubuntu.

---

## Part 1: Installing Webmin on Ubuntu

Webmin is a web-based interface for managing Unix-like systems, making tasks such as user management, server configuration, and software installation easier.

### Step 1: Update Your System

Before installing Webmin, update your system to ensure all packages are up to date.

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2: Add the Webmin Repository and Key

To add the Webmin repository, download and run the setup script.

```bash
curl -o setup-repos.sh https://raw.githubusercontent.com/webmin/webmin/master/setup-repos.sh
sudo sh setup-repos.sh
```

### Step 3: Install Webmin

With the repository set up, install Webmin:

```bash
sudo apt-get install webmin --install-recommends
```

### Step 4: Access Webmin

Once installed, Webmin runs on port 10000. You can access it by opening a browser and navigating to:

```
https://<your-server-ip>:10000
```

If you are using a firewall, allow traffic on port 10000:

```bash
sudo ufw allow 10000
```

You can now log in to Webmin using your system's root credentials.

---

## Part 2: Expanding a Logical Volume Using Webmin

Expanding a logical volume through Webmin’s Logical Volume Management (LVM) interface is a simple process.

### Step 1: Access Logical Volume Management

Log in to Webmin and navigate to:

**Hardware > Logical Volume Management**

Here, you can manage physical volumes, volume groups, and logical volumes.

### Step 2: Add a New Physical Volume

If you've added a new disk or partition to your system, you need to allocate it to a volume group before expanding the logical volume. To do this:
1. Locate your volume group in the Logical Volume Management module.
2. Click **Add Physical Volume**.
3. Select the new partition or RAID device and click **Add to volume group**. This action increases the available space in the group.

### Step 3: Resize the Logical Volume

To extend a logical volume:
1. In the **Logical Volumes** section, locate the logical volume you wish to extend.
2. Select **Resize**.
3. Specify the additional space or use all available free space in the volume group.
4. Click **Apply** to resize the logical volume.

### Step 4: Resize the Filesystem

After resizing the logical volume, expand the filesystem to match:
1. Click on the logical volume to view its details.
2. For supported filesystems like ext2, ext3, or ext4, click **Resize Filesystem**. The filesystem will automatically adjust to the new size of the logical volume.

---

## Part 3: Installing Docker on Ubuntu

This section covers installing Docker on Ubuntu.

### Step 1: Remove Older Versions

If you have previous versions of Docker installed, remove them:

```bash
sudo apt remove docker docker-engine docker.io containerd runc
```

### Step 2: Add Docker's Official GPG Key and Repository

Add Docker’s GPG key and repository to your system’s Apt sources:

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
```

### Step 3: Install Docker

Now, install Docker:

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### Step 4: Post-Installation Steps

To allow your user to run Docker commands without `sudo`, add your user to the Docker group:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

Test your Docker installation by running the following command:

```bash
docker run hello-world
```

For more information, visit the official [Docker installation page](https://docs.docker.com/engine/install/ubuntu/).