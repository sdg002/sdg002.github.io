# Developing and deploying a Python Azure Function - Step by step
---

# Why did I write this?
I wanted to come to terms with developing and deploying a Python Azure Function. I have been working with C# Azure Functions for a quite a while now. Phython development is different from C#. Python has its nuances. In this article, I have documented the steps I took to build and deploy a simple "Hello world" Python Azure Function. In the accompanying code, I have demonstrated a simple REST end point (also known as  Http trigger)

---

# What was my business scenario?
I am working with a team of quantitative analysts who were looking for ways to migrate their free standing python web scraper scripts from on premise servers to Azure. These are scripts which run periodically,every few hours and scrape financial information from web sites. This information is dumped out into CSV files. I considered the following options:
1. Continous Azure Web job
1. Docker
1. Http trigger in an Azure function (orchestrated by a Azure Data Factory pipeline)

---

# Python Azure Functions - What is the big picture?

![flowchart](docs/images/flow_chart.png)

You will need the following tools. All of which are freely downloadable from Microsoft
- Visual Studio Code
- Azure Functions Core Tools
- Visual Studio Extensions for Azure Functions
- PowerShell Core
- Visual Studio Extensions for PowerShell
- Azure CLI
- Azure PowerShell modules (Az.Accounts,Az.Functions)

---
# Understanding Azure Function Core Tools

<<What is this tool? Why is it neccessary? How to download? Show a picture>>

---
# What should be the overall folder structure?

<<show a pic of the folder tree, with explanation of what goes where>>

---
# How does a Python function end point work?

<< explain the structure of a single end point, with folder view>>

---
# Step 0 - Determine which Python runtime to support 

You are limited by what Azure has to offer!
to be done

# Step 1 - Using Azure Function Core Tools to create the skeletal structure
to be done

---
# Step 2 - Using Azure Function Core Tools to add a Http function end point

to be done

---

# Step 3 - Debugging the Python function using Azure Function Core Tools
to be done

---

# Step 4- Using PowerShell and Azure to CLI to deploy the Python function to an Azure functionapp

<<show a picture of the deployment, show arrows, which PowerShell does what >>

---
# Step 5 - Ensuring that Unit tests are discovered

<< Talk about PYTHONPATH, show a picture of Test explorer with and without PYTHONPATH, how would you solve this>>
---

# References to docs on Microsoft
to be done

---

# Appendix
---


---

-----
# Overview
- Demonstrates a Python Azure Function
- Demonstrates a Infrastructure script to deploy the Azure function to the cloud
- We are not doing the CI configuration using Jenkins or Azure Devops, however we intend to have a single PowerShell script ready for CI

---
# Current deployment
- https://pythonfunc001.azurewebsites.net/api/HttpTrigger1?name=john
- https://pythonfunc001.azurewebsites.net/api/Add?num1=100&num2=300.55
---

# Pending Tasks
- ~~Look into the desired folder strucutre~~
- ~~Create a skeletal working Azure function~~
- ~~Add trigger to add 2 numbers~~
- ~~Test the trigger locally~~
- ~~Structure the folder to keep the Math lib outside~~
- ~~Deploy to Azure~~
- Write some unit tests
~~- How to set configuration settings on Azure?~~
- Write a PowerShell script to run the unit tests and run PEP8 (under build folder)
- 

---
 
# Recommended folder structure by Microsoft
As per [guidance from Microsoft](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=asgi%2Cazurecli-linux%2Capplication-level#folder-structure),
```
 <project_root>/
 | - .venv/
 | - .vscode/
 | - my_first_function/
 | | - __init__.py
 | | - function.json
 | | - example.py
 | - my_second_function/
 | | - __init__.py
 | | - function.json
 | - shared_code/
 | | - __init__.py
 | | - my_first_helper_function.py
 | | - my_second_helper_function.py
 | - tests/
 | | - test_my_second_function.py
 | - .funcignore
 | - host.json
 | - local.settings.json
 | - requirements.txt
 | - Dockerfile
```
---

# Steps for creating a skeletal Azure Function
- Ensure you have the **[Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local)** tool installed
- Ensure you have the **Azure Functions Extensions** for Visual Studio Code installed
- Click on the **New Project** icon and respond to the questions from the wizard
- 
![New Azure Function](docs/images/vscode_new_azurefunc.png)

---

# References
- [Quickstart: Create a Python function in Azure from the command line](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=azure-cli%2Cbash%2Cbrowser)
- [Quickstart: Create a function in Azure with Python using Visual Studio Code](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python)
- [Configure a Linux Python app for Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/configure-language-python)
- ??
- [Azure Functions Python developer guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
- ??
- 
- 

---

# How to deploy the Azure Function?
## Python is different from .NET or NodeJS
In case of Python, there is no build command (unlike C# or NodeJS). Therefore you will need to publish the raw contents. But,we must remember that the project directory has lots of files which are not to be deployed. E.g. the `.venv` directory.

## The publish command
You will need to use the Azure Function Core tool as follows:
```powershell
func azure functionapp publish [name of the function app]
```
The function app should have been created prior to the above step using methods like `az functionapp plan create` and `az functionapp create`

## Setting the Azure Context correctly (add to Appendix)
Before you run the publish command, the Azure subscription must have been set correctly. This is neccessary for Azure Function Core tool to detect the function app.  Run the following commands to ensure you are console is pointing to the right subscription. 
```powershell
az account show
```

```powershell
Get-AzContext
```

## Further reference on Azure Function Core tools
Follow [this link](https://docs.microsoft.com/en-us/azure/azure-functions/functions-core-tools-reference?tabs=v2#func-azure-functionapp-publish) for more details on how to use the **Func** tool

---

You were reading this https://docs.microsoft.com/en-us/azure/azure-functions/functions-core-tools-reference?tabs=v2#func-azure-functionapp-fetch-app-settings

You were trying the following, it did not work, needs functionapp names
```
func azure functionapp publish  --list-ignored-files
```

---


# Appendix
## How to set Configuration parameters on Azure?
Example snippet below:
```powershell
    $settings=@{"name1"="value1"; "name2"="blah2"; "name3"="blah3"}
    Update-AzFunctionAppSetting -ResourceGroupName  $ResourceGroup -Name $FunctionApp -AppSetting $settings
```

Refer [documentation](https://docs.microsoft.com/en-us/azure/azure-functions/functions-how-to-use-azure-function-app-settings?tabs=azure-powershell#settings) from Microsoft

## How to specify the Python version of the Azure function app?
The commandline option `functions-version` of `az functionapp create` specifies the Python engine version
```powershell
az functionapp create --name $FunctionApp --resource-group $ResourceGroup --plan $FunctionAppPlan --storage-account $FunctionStorageAccount --runtime python --runtime-version 3.8 --functions-version 3 --disable-app-insights
```

# How to find the supported Python versions on Azure?
Why is this important? Your local development environment is restricted by the runtimes supported on Azure.
```powershell
az webapp list-runtimes 
```
Sample output as of April 2022:
```json
{
  "linux": [
    "DOTNETCORE:6.0",    
    "DOTNETCORE:5.0",    
    "DOTNETCORE:3.1",    
    "NODE:16-lts",       
    "NODE:14-lts",       
    "NODE:12-lts",       
    "PYTHON:3.9",        
    "PYTHON:3.8",        
    "PYTHON:3.7",        
    "PHP:8.0",
    "PHP:7.4",
    "RUBY:2.7",
    "RUBY:2.7.3",        
    "JAVA:11-java11",    
    "JAVA:8-jre8",       
    "JBOSSEAP:7-java11", 
    "JBOSSEAP:7-java8",  
    "TOMCAT:10.0-java11",
    "TOMCAT:10.0-jre8",  
    "TOMCAT:9.0-java11", 
    "TOMCAT:9.0-jre8",   
    "TOMCAT:8.5-java11",
    "TOMCAT:8.5-jre8"
  ],
  "windows": [
    "dotnet:6",
    "dotnet:5",
    "DOTNETCORE:3.1",
    "ASPNET:V4.8",
    "ASPNET:V3.5",
    "NODE:16LTS",
    "NODE:14LTS",
    "NODE:12LTS",
    "PHP:7.4",
    "java:1.8:Java SE:8",
    "java:11:Java SE:11",
    "java:1.8:TOMCAT:10.0",
    "java:11:TOMCAT:10.0",
    "java:1.8:TOMCAT:9.0",
    "java:11:TOMCAT:9.0",
    "java:1.8:TOMCAT:8.5",
    "java:11:TOMCAT:8.5"
  ]
}
```

## Why is it neccessry to set the PYTHONPATH environment variable ?
You have re-usable classes under the folder **shared_code**. You have unit tests which are outside the **shared_code** hierarchy. How do the unit tests recognize modules inside the **shared_code** folder? 

- You need to set this before launching VS code
- VS Code must inherit this variable

```
<project_root>/
 | - my_first_function/
 | | - __init__.py
 | | - function.json
 | | - example.py
 | - my_second_function/
 | | - __init__.py
 | | - function.json
 | - shared_code/
 | | - __init__.py
 | | - my_first_helper_function.py
 | | - my_second_helper_function.py
 | - tests/
 | | - test_my_second_function.py
 
```
```bash
set PYTHONPATH=<absolute folder of project_root>
```
Unit tests should have the following imports
```python
from shared_code import my_first_helper_function
```
