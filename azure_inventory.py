import subprocess
import sys
import os

def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        print(f"Failed to install {package} with error: {e}")

# Install the necessary packages
install("azure-mgmt-resource")
install("azure-identity")

def azure_resources():
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
        config.load_kube_config("~/.kube/config")
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
    azure_resources()
    kubernetes_pods()
