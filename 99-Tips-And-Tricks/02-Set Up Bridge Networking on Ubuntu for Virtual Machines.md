### **Guide to Set Up Bridge Networking on Ubuntu for Virtual Machines**

This guide explains how to configure bridge networking on Ubuntu to allow virtual machines (VMs) to directly access the network, obtaining their own IP addresses from the DHCP server.

By following this guide, you can successfully set up bridge networking, enabling your virtual machines to directly access the network as if they were standalone devices.

---

#### **Step 1: Identify Your Primary Network Interface**
The primary network interface is the one currently used by the server for network access. Identify it with the following command:

```bash
ip link show
```

Look for the name of the interface (e.g., `enp8s0`) with `state UP`.

---

#### **Step 2: Backup Your Current Network Configuration**
Before making any changes, back up the existing netplan configuration file:

```bash
sudo cp /etc/netplan/00-installer-config.yaml /etc/netplan/00-installer-config.yaml.bak
```

---

#### **Step 3: Configure the Bridge**
Edit the netplan configuration file:

```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

Replace its content with the following, adjusted for your environment:

```yaml
network:
  version: 2
  ethernets:
    enp8s0:
      dhcp4: no
  bridges:
    br0:
      interfaces: [enp8s0]
      dhcp4: true
```

- `enp8s0`: Your physical network interface.
- `br0`: The new bridge interface that will be used by the virtual machines and the host.

Save and exit the file.

---

#### **Step 4: Apply the Configuration**
Apply the new network configuration to create the bridge:

```bash
sudo netplan apply
```

---

#### **Step 5: Verify the Bridge Configuration**
Check that the bridge `br0` is active and has an IP address:

```bash
ip addr show br0
```

You should see an output like this:

```plaintext
3: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 46:10:cc:63:f4:37 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.10/24 metric 100 brd 192.168.1.255 scope global dynamic br0
       valid_lft 7102sec preferred_lft 7102sec
```

---

#### **Step 6: Configure Virtual Machines to Use the Bridge**
For VMs created with tools like `virt-manager` or `virsh`:
1. When configuring the VM’s network interface, choose **Bridge** as the network source.
2. Set `br0` as the bridge interface.
3. The VM will now obtain an IP address dynamically from the same DHCP server as the host.

For `virt-manager`:
- Go to **Add Hardware > Network**.
- Choose **Bridge br0** as the source.

---

#### **Step 7: Test the Setup**
1. Start a VM and ensure it obtains a dynamic IP address from the network.
2. Test connectivity by pinging the gateway or external servers from the VM.

---

### **Key Considerations**
1. **Dynamic IP for Host:** The host server's IP address will now be associated with the bridge (`br0`) instead of the physical interface (`enp8s0`). This is expected behavior.
2. **Backup Configuration:** Always maintain a backup of your original network configuration to revert changes if needed.
3. **Network Manager vs. Netplan:** Use only one method (`netplan` or `nmcli`) for managing network configurations to avoid conflicts.
4. **Alternative Access:** If you are working on a remote server, ensure alternative access (e.g., a second network interface) before applying network changes.

