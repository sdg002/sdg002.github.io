Set-StrictMode -Version "2.0"
$ErrorActionPreference="Stop"

$ResourceGroup="rg-demo-python-func"
$Location="uksouth"
$FunctionAppPlan="MyDemoPythonFunctionAppPlan"
$FunctionSku="B1"  #Y1 was not allowed
$FunctionApp="PythonFunc001"
$FunctionStorageAccount="mypythonfunctionapp001"

function CreateResourceGroup()
{
    Write-Host "Creating resource group $ResourceGroup"
    az group create --name $ResourceGroup --location  $Location | Out-Null
}
function CreateFuntionAppPlan()
{
    Write-Host "Creating functionapp plan $FunctionAppPlan"
    az functionapp plan create --name $FunctionAppPlan --location $Location --resource-group $ResourceGroup  --sku $FunctionSku --min-instances 2  --is-linux $true | Out-Null
}

function CreateFuntionApp()
{
    Write-Host "Creating storage account $FunctionStorageAccount"
    az storage account create --name $FunctionStorageAccount --resource-group $ResourceGroup --location $Location --sku "Standard_LRS"
    Write-Host "Creating function app $FunctionApp in the plan: $FunctionAppPlan"
    az functionapp create --name $FunctionApp --resource-group $ResourceGroup --plan $FunctionAppPlan --storage-account $FunctionStorageAccount --runtime python --runtime-version 3.8 --functions-version 3 --disable-app-insights
}
function DeployFunctionApp()
{
    Write-Host "Deploying file to the function app"
    $scriptFolder=$PSScriptRoot
    $srcFolder=Join-Path -Path $scriptFolder -ChildPath "..\src\"
    Push-Location -Path $srcFolder
    & func azure functionapp publish $FunctionApp
    Pop-Location
}

function SetConfigurationSettings()
{
    Write-Host "Setting configuration settings"
    $settings=@{"name1"="value1"; "name2"="blah2"; "name3"="blah3"}
    Update-AzFunctionAppSetting -ResourceGroupName  $ResourceGroup -Name $FunctionApp -AppSetting $settings
}

CreateResourceGroup
CreateFuntionAppPlan
CreateFuntionApp
DeployFunctionApp
SetConfigurationSettings
