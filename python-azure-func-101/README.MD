# Overview
- Demonstrates a Python Azure Function
- Demonstrates a Infrastructure script to deploy the Azure function to the cloud
- We are not doing the CI configuration using Jenkins or Azure Devops, however we intend to have a single PowerShell script ready for CI
- We are not doing the CD configuration using Jenkins or Azure Devops, however we intend to have a single PowerShell script ready for CI

# Tasks
- Look into the desired folder strucutre
- Create a skeletal working Azure function
- Add trigger to add 2 numbers
- Test the trigger locally
- Structure the folder to keep the Math lib outside
- Write some unit tests
- Deploy to Azure
- Write a PowerShell script to run the unit tests, run PEP8
- 
- 
# Recommended folder structure
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
# Steps for creating a skeletal Azure Function
To be done. See One note

# References
- [Quickstart: Create a Python function in Azure from the command line](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=azure-cli%2Cbash%2Cbrowser)
- [Quickstart: Create a function in Azure with Python using Visual Studio Code](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python)
- [Configure a Linux Python app for Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/configure-language-python)
- ??
- [Azure Functions Python developer guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
- ??
- 