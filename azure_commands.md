# **Download the Azure CLI on Windows and Install**
#### Downloading and Installing the Azure CLI
```Invoke-WebRequest -Uri https://aka.ms/installazurecliwindowsx64 -OutFile .\AzureCLI-x64.msi```
or
```$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://aka.ms/installazurecliwindowsx64 -OutFile .\AzureCLI-x64.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI-x64.msi /quiet'; Remove-Item .\AzureCLI-x64.msi```

#### Invoke the MSI installer suppressing all output
```Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI-x64.msi /quiet'```
#### Remove the MSI installer
```Remove-Item -Path .\AzureCLI-x64.msi```

# **Azure Login and Subscription Information**
#### Login in CLI
```az login```
#### List accounts
```az account list```
#### Set subscription
```az account set --subscription "xxx"```

# **Creating a basic VM**
#### Get all available VM sizes
```az vm list-sizes --location eastus```
#### Get all available VM images for Windows and Linux
```az vm image list --output table```
#### Create a Linux VM
```az vm create --resource-group labrg-1137911 --name myVM-1137911 --image Ubuntu2204 --generate-ssh-keys```
#### Create a Windows VM
```az vm create --resource-group myResourceGroup --name myVM --image win2016datacenter```
#### Create a Storage account.
```az storage account create -g myresourcegroup -n mystorageaccount -l eastus --sku Standard_LRS```

# **Managing VMs**
#### List your VMs
```az vm list```
#### Start a VM
```az vm start --resource-group myResourceGroup --name myVM```
#### Stop a VM
```az vm stop --resource-group myResourceGroup --name myVM```
#### Restart a VM
```az vm restart --resource-group myResourceGroup --name myVM```
#### Redeploy a VM
```az vm redeploy --resource-group myResourceGroup --name myVM```
#### Delete a VM
```az vm delete --resource-group labrg-xxxx --name myVM-xxxx```
#### Create an image of a VM
```az image create --resource-group myResourceGroup --source myVM --name myImage```
#### Associate Batch with a storage account.
```az batch account set -g myresourcegroup -n mybatchaccount --storage-account mystorageaccount```
#### Authenticate directly against the account for further CLI interaction
```az batch account login -g myresourcegroup -n mybatchaccount```
#### Display the details of our created account
```az batch account show -g myresourcegroup -n mybatchaccount```

# **Application Management**
#### Create a new application
```az batch application create --resource-group myresourcegroup --name mybatchaccount --application-id myapp --display-name "My Application"```
