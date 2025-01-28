# restaurant-manager-api

### CICD pipeline

#### Infrastructur - Terraform
1. Prepare an Azure service principal with a secret: 
    ```
    az ad sp create-for-rbac --name "my-service-principal" --role contributor --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group-name}
    ```
    ```
    output:
    {
    "appId": "your-client-id",
    "displayName": "my-service-principal",
    "password": "your-client-secret",
    "tenant": "your-tenant-id"
    }
    ```
    ```
    az role assignment create --assignee <SP-Client-ID> --role Contributor --scope /subscriptions/{subscription-id}/resourceGroups/{resource-group-name}
    ```
1. Create GitHub Action Secrets, using the previous step output:
    - AZURE_CLIENT_ID (appId)
    - AZURE_CLIENT_SECRET (password)
    - AZURE_SUBSCRIPTION_ID
    - AZURE_TENANT_ID

    Choose values which stands with Azure policy and save them also to Github Action Secrets for:
    - SQL_ADMIN_PASSWORD
    - SQL_ADMIN_USERNAME

#### Pipeline - Service app
1. Get 'publish profile' from Azure App Service: _Azure Portal -> App Service > Get publish profile_
1. Create Github Action Secrets
    - AZURE_CONTAINER_REGISTRY: Your Azure Container Registry name (without .azurecr.io).
    - ACR_USERNAME: The username for your Azure Container Registry. (Usually in the form of a service principal or admin user).
    - ACR_PASSWORD: The password for your Azure Container Registry (stored in the form of a secret).
    - AZURE_APP_SERVICE_PUBLISH_PROFILE: The publish profile from your Azure App Service
    - APPLICATION_INSIGHTS_INSTRUMENTATION_KEY: The Instrumentation Key from existing Azure Application Insights resource.


---

### Terraform
1. Configure the Terraform Azure provider (main.tf)
    - azurerm
1. Configure varibles (variables.tf, terraform.tfvars - marked, using github action secrets and pipeline envs instead) 
1. Create and add an Azure resource group (main.tf)
    - Resource group
    - Resources - plan, serviceapp, sql server, db, firewall
    - Firewall - should restrict access to known IPs or Azure services
    - SKU - plan & db - assume using tier "Standard" , size = "S1"
1. Configure output in main.tf
1. Expected output:
    ```
    Apply complete! Resources: 6 added, 0 changed, 0 destroyed.

    Outputs:

    app_service_url = "restaurant-recommendation-appservice.azurewebsites.net"
    sql_server_admin_login = "adminuser"
    sql_server_fqdn = "restaurant-sql-server.database.windows.net"
    sql_database_connection_string = <sensitive>
    ```

---

### Python
Swagger http://restaurant-recommendation-appservice.azurewebsites.net/docs#/

Get recommandation:
1. Go to Swagger
1. Get /find_restaurant, click on 'Try it out'
1. Fill your sentence in sentenct box or use the given example 'An italian restaurant that opens at 08:00 vegi'
1. Expected output: 
    ```
    [ "{\"name\": \"Green Bowl\", \"style\": \"Italian\", \"address\": \"Veggie Street 15, Ramat-Gan\", \"open_hour\": \"08:00\", \"close_hour\": \"22:00\", \"vegetarian\": \"yes\", \"delivery\": \"yes\"}"] 
    ```

### Unit Tests
* 2 tests files, for db.py and service.py
* Run via pipeline, output is saved in tests/test-results.xml

---

###  Details
Requirement | Solution / Implementation Details
--- | --- 
The system has to be cloud-native, with a preference for Azure with a simple architecture that will require a minimal amount of maintenance | Used Azure sql and Azure service app, together they ensure minimal maintenance while providing a reliable and secure environment for the cloud-native system
The system should be written in full IaC style. Use Terraform for configuring the required cloud resources | I used Terraform with variables to define the system's infrastructure as code, ensuring consistent and flexible provisioning of Azure resources
There should be some backend storage mechanism that holds the history of all requests and returned responses. a. Consider that the backend data stored is highly confidential | I used Python with pyodbc to connect to Azure SQL for storing request and response histories. To ensure confidentiality, I encrypted sensitive data using the cryptography library and managed environment variable to pass the connection string. 
Improvement | OPTIONAL: for better data protection, use 'Azure SQL Always Encrypted' and add it to db_connection_string
Make sure the system is secure. a. However, there is no need for the user to authenticate with the system (Assume it’s a free public service) | Secured DB (using encryption), Using secrets instead of hardcoded credenials, Azure service principal, Azure firewall to restrict access to known IPs or Azure services
Improvement | OPTIONAL: Sign docker images 
The system code should be deployed using an automatic CI\CD pipeline following any code change, including when adding or updating restaurants | I set up a CI/CD pipelines to automate infrastructure provisioning with Terraform and deploy Python code to Azure App Service, ensuring updates with every code change.
The code should be ready for code review (as possible) | Unittests, logger, comments
Coding: Python \ PowerShell |  The application is written in Python using FastAPI for a clean, fast, and modern API design. Swagger is automatically provided.
Improvement | OPTIONAL: Improve the accuracy of results and efficiency of parser functions in Python code 
    
