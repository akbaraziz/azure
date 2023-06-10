import subprocess
import os
import sys

def is_tool_installed(name):
    try:
        devnull = open(os.devnull)
        subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True

def install_kubectl():
    try:
        run_command("curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl")
        run_command("chmod +x ./kubectl")
        run_command("sudo mv ./kubectl /usr/local/bin/kubectl")
    except Exception as e:
        print(f"Failed to install kubectl with error: {e}")
        sys.exit(1)

def run_command(command):
    try:
        output = subprocess.check_output(command, shell=True)
        return output
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error: {e}")
        sys.exit(1)

def get_kubeconfig(resource_group, cluster_name, file_name):
    command = f"az aks get-credentials --resource-group {resource_group} --name {cluster_name} --file {file_name}"
    run_command(command)

def merge_kubeconfigs(file_names, output_file):
    command = f"KUBECONFIG={':'.join(file_names)} kubectl config view --flatten > {output_file}"
    run_command(command)

if __name__ == "__main__":
    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    if not subscription_id:
        print("Please set the AZURE_SUBSCRIPTION_ID environment variable.")
        sys.exit(1)

    # Check if kubectl is installed, if not, install it
    if not is_tool_installed("kubectl"):
        install_kubectl()

    # Log in to Azure
    run_command("az login")

    # Set the Azure subscription
    run_command(f"az account set --subscription {subscription_id}")

    # Get the kubeconfig for each cluster
    clusters = [
        {"resource_group": "<resource-group-1>", "cluster_name": "<cluster-name-1>", "file_name": "./kubeconfig1"},
        {"resource_group": "<resource-group-2>", "cluster_name": "<cluster-name-2>", "file_name": "./kubeconfig2"},
        # Add more clusters as needed
    ]
    for cluster in clusters:
        get_kubeconfig(cluster["resource_group"], cluster["cluster_name"], cluster["file_name"])

    # Merge the kubeconfig files
    merge_kubeconfigs([cluster["file_name"] for cluster in clusters], "./merged-kubeconfig")
