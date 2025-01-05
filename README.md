# restaurant-manager-api

### CICD pipeline

#### Infrastructur - Terraform
1. Prepare an Azure service principal with a secret: 
```
az ad sp create-for-rbac --name "my-service-principal" --role contributor --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group-name}

output:
{
  "appId": "your-client-id",
  "displayName": "my-service-principal",
  "password": "your-client-secret",
  "tenant": "your-tenant-id"
}

az role assignment create --assignee <SP-Client-ID> --role Contributor --scope /subscriptions/{subscription-id}/resourceGroups/{resource-group-name}
```
1. Create GitHub Action secrets, using the previous step output:
`AZURE_CLIENT_ID (appId), AZURE_CLIENT_SECRET (password), AZURE_SUBSCRIPTION_ID, AZURE_TENANT_ID`
* Choose values which stands with Azure policy for `SQL_ADMIN_PASSWORD, SQL_ADMIN_USERNAME` and save them also to Github Action Secrets


#### Pipeline - Service app
1. Get 'publish profile' from Azure App Service: Azure Portal -> App Service > Get publish profile
1. Create Github Action Secrets
```
AZURE_CONTAINER_REGISTRY: Your Azure Container Registry name (without .azurecr.io).
ACR_USERNAME: The username for your Azure Container Registry. (Usually in the form of a service principal or admin user).
ACR_PASSWORD: The password for your Azure Container Registry (stored in the form of a secret).
AZURE_APP_SERVICE_PUBLISH_PROFILE: The publish profile from your Azure App Service
APPLICATION_INSIGHTS_INSTRUMENTATION_KEY: The Instrumentation Key from existing Azure Application Insights resource.
```

---

### Terraform
1. Configure the Terraform Azure provider (main.tf)
    1. azurerm
1. Configure varibles (variables.tf, terraform.tfvars - marked, using github action secrets and pipeline envs instead) 
1. Create and add an Azure resource group (main.tf)
    1. Resource group
    1. Resources - plan, serviceapp, sql server, db, firewall
    1. Firewall - should restrict access to known IPs or Azure services
    1. SKU - plan & db - assume using tier "Standard" , size = "S1"
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
1. Expected output: `[ "{\"name\": \"Green Bowl\", \"style\": \"Italian\", \"address\": \"Veggie Street 15, Ramat-Gan\", \"open_hour\": \"08:00\", \"close_hour\": \"22:00\", \"vegetarian\": \"yes\", \"delivery\": \"yes\"}"]`

### Unit Tests
* 2 tests files, for db.py and service.py
* Run via pipeline, output is saved in tests/test-results.xml

---

### Improvement options
1. Use 'Azure SQL Always Encrypted' and add it to db_connection_string instead of using encryption library
1. Sign docker images
