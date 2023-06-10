# This script requires the following to be installed:
# - Python 3
# - Azure CLI
# - kubectl
#
# The following Python packages are required and will be installed by the script:
# - azure-mgmt-resource
# - azure-identity
# - kubernetes
#
# The following environment variables need to be set:
# - AZURE_SUBSCRIPTION_ID: The ID of your Azure subscription.
#
# The script also requires the following information about your Azure Kubernetes clusters:
# - Resource group name
# - Cluster name
#
# This information should be added to the `clusters` list in the script in the following format:
# {"resource_group": "<resource-group>", "cluster_name": "<cluster-name>", "file_name": "./kubeconfig"}
# Replace <resource-group> and <cluster-name> with the resource group and name of your cluster.
# The file_name is the name of the kubeconfig file that will be created for the cluster.
# Add an entry to the list for each cluster.


import subprocess
import os
import sys

def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        print(f"Failed to install {package} with error: {e}")

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

def azure_resources():
    install("azure-mgmt-resource")
    install("azure-identity")
    try:
        from azure.identity import DefaultAzureCredential
        from azure.mgmt.resource import ResourceManagementClient
    except ImportError as e:
        print(f"Failed to import Azure modules with error: {e}")
        sys.exit(1)

    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    if not subscription_id:
        print("Please set the AZURE_SUBSCRIPTION_ID environment variable.")
        sys.exit(1)

    try:
        credential = DefaultAzureCredential()
        resource_client = ResourceManagementClient(credential, subscription_id)
        resources = resource_client.resources.list()
    except Exception as e:
        print(f"Failed to get Azure resources with error: {e}")
        return

    resource_count = {}

    for resource in resources:
        if resource.type in resource_count:
            resource_count[resource.type] += 1
        else:
            resource_count[resource.type] = 1

    for resource_type, count in resource_count.items():
        print(f"{resource_type}: {count}")

def kubernetes_pods():
    install("kubernetes")
    try:
        from kubernetes import client, config
    except ImportError as e:
        print(f"Failed to import Kubernetes modules with error: {e}")
        sys.exit(1)

    try:
        # Load the kubeconfig file (replace with the path to your kubeconfig file)
        config.load_kube_config("./merged-kubeconfig")
        v1 = client.CoreV1Api()
        pods = v1.list_pod_for_all_namespaces(watch=False)
    except Exception as e:
        print(f"Failed to get Kubernetes pods with error: {e}")
        return

    namespace_pod_count = {}

    for pod in pods.items:
        if pod.metadata.namespace in namespaceIt seems like the response was cut off. Here's the complete script:

```python
import subprocess
import os
import sys

def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        print(f"Failed to install {package} with error: {e}")

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

def azure_resources():
    install("azure-mgmt-resource")
    install("azure-identity")
    try:
        from azure.identity import DefaultAzureCredential
        from azure.mgmt.resource import ResourceManagementClient
    except ImportError as e:
        print(f"Failed to import Azure modules with error: {e}")
        sys.exit(1)

    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    if not subscription_id:
        print("Please set the AZURE_SUBSCRIPTION_ID environment variable.")
        sys.exit(1)

    try:
        credential = DefaultAzureCredential()
        resource_client = ResourceManagementClient(credential, subscription_id)
        resources = resource_client.resources.list()
    except Exception as e:
        print(f"Failed to get Azure resources with error: {e}")
        return

    resource_count = {}

    for resource in resources:
        if resource.type in resource_count:
            resource_count[resource.type] += 1
        else:
            resource_count[resource.type] = 1

    for resource_type, count in resource_count.items():
        print(f"{resource_type}: {count}")

def kubernetes_pods():
    install("kubernetes")
    try:
        from kubernetes import client, config
    except ImportError as e:
        print(f"Failed to import Kubernetes modules with error: {e}")
        sys.exit(1)

    try:
        # Load the kubeconfig file (replace with the path to your kubeconfig file)
        config.load_kube_config("./merged-kubeconfig")
        v1 = client.CoreV1Api()
        pods = v1.list_pod_for_all_namespaces(watch=False)
    except Exception as e:
        print(f"Failed to get Kubernetes pods with error: {e}")
        return

    namespace_pod_count = {}

    for pod in pods.items:
        if pod.metadata.namespace in namespace_podApologies for the cut-off in the previous message. Here's the complete `kubernetes_pods` function and the main execution of the script:

```python
def kubernetes_pods():
    install("kubernetes")
    try:
        from kubernetes import client, config
    except ImportError as e:
        print(f"Failed to import Kubernetes modules with error: {e}")
        sys.exit(1)

    try:
        # Load the kubeconfig file
        config.load_kube_config("./merged-kubeconfig")
        v1 = client.CoreV1Api()
        pods = v1.list_pod_for_all_namespaces(watch=False)
    except Exception as e:
        print(f"Failed to get Kubernetes pods with error: {e}")
        return

    namespace_pod_count = {}

    for pod in pods.items:
        if pod.metadata.namespace in namespace_pod_count:
            namespace_pod_count[pod.metadata.namespace] += 1
        else:
            namespace_pod_count[pod.metadata.namespace] = 1

    for namespace, count in namespace_pod_count.items():
        print(f"{namespace}: {count} pods")

if __name__ == "__main__":
    # Check if kubectl is installed, if not, install it
    if not is_tool_installed("kubectl"):
        install_kubectl()

    # Log in to Azure
    run_command("az login")

    # Set the Azure subscription
    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    if not subscription_id:
        print("Please set the AZURE_SUBSCRIPTION_ID environment variable.")
        sys.exit(1)
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

    # Perform Azure resources inventory
    azure_resources()

    # Perform Kubernetes pods inventory
    kubernetes_pods()
