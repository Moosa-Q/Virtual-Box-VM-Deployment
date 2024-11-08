import subprocess

# Display available OS types
print("Available OS types for VirtualBox:")
print("1. Ubuntu_64")
print("2. Linux_64")
print("3. Debian_64")
print("4. OpenSUSE_64")
print("5. Windows10_64")
print("6. MacOS_64")
print("7. Kali_Linux (Linux24_64)")

# Prompt for VM configuration details
vm_name = input("Enter VM name (avoid spaces): ")
os_choice = input("Enter OS type number (1-7): ")
cpu_count = int(input("Enter number of CPUs: "))
memory_size = int(input("Enter memory size in MB: "))
disk_size_gb = int(input("Enter disk size in GB: "))
iso_path = input("Enter the full path to the ISO file (or leave blank to skip): ")

# Map the OS choice to VBoxManage OS types
os_type_map = {
    "1": "Ubuntu_64",
    "2": "Linux_64",
    "3": "Debian_64",
    "4": "OpenSUSE_64",
    "5": "Windows10_64",
    "6": "MacOS_64",
    "7": "Linux24_64"  # Updated for Kali Linux
}
os_type = os_type_map.get(os_choice, "Ubuntu_64")  # Default to "Ubuntu_64" if choice is invalid

# Convert disk size from GB to MB
disk_size_mb = disk_size_gb * 1024

# Attempt to create a new VM
print(f"Creating VirtualBox VM named '{vm_name}' with OS type '{os_type}'...")
result = subprocess.run(["VBoxManage", "createvm", "--name", vm_name, "--ostype", os_type, "--register"], capture_output=True, text=True)

if result.returncode != 0:
    print("Error creating VM:", result.stderr)
else:
    # Configure VM settings if creation was successful
    print(f"Setting CPU count to {cpu_count}, memory to {memory_size} MB...")
    subprocess.run(["VBoxManage", "modifyvm", vm_name, "--cpus", str(cpu_count), "--memory", str(memory_size), "--vram", "16"])

    # Create and attach a virtual hard disk
    print(f"Creating virtual hard disk of size {disk_size_mb} MB...")
    disk_path = f"{vm_name}.vdi"
    subprocess.run(["VBoxManage", "createmedium", "disk", "--filename", disk_path, "--size", str(disk_size_mb), "--format", "VDI"])
    subprocess.run(["VBoxManage", "storagectl", vm_name, "--name", "SATA Controller", "--add", "sata", "--controller", "IntelAhci"])
    subprocess.run(["VBoxManage", "storageattach", vm_name, "--storagectl", "SATA Controller", "--port", "0", "--device", "0", "--type", "hdd", "--medium", disk_path])

    # Add an IDE controller for attaching the ISO file
    subprocess.run(["VBoxManage", "storagectl", vm_name, "--name", "IDE Controller", "--add", "ide"])

    # Attach ISO file if path is provided
    if iso_path:
        print(f"Attaching ISO file '{iso_path}' to IDE controller...")
        iso_attach_result = subprocess.run(["VBoxManage", "storageattach", vm_name, "--storagectl", "IDE Controller", "--port", "1", "--device", "0", "--type", "dvddrive", "--medium", iso_path], capture_output=True, text=True)
        if iso_attach_result.returncode != 0:
            print("Error attaching ISO file:", iso_attach_result.stderr)

    # Start the VM
    print(f"Starting VirtualBox VM '{vm_name}'...")
    start_result = subprocess.run(["VBoxManage", "startvm", vm_name, "--type", "headless"], capture_output=True, text=True)
    if start_result.returncode != 0:
        print("Error starting VM:", start_result.stderr)
    else:
        print(f"VirtualBox VM '{vm_name}' has been created and started successfully!")
