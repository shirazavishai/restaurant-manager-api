# restaurant-manager-api

### Python
Swagger http://127.0.0.1:8000/docs#/

Get recommandation:
1. Go to Swagger
1. Get /find_restaurant, click on 'Try it out'
1. Fill your sentence in param box 'An italian restaurant that opens at 08:00 vegi'
1. Execute ==> `[
  "{\"name\": \"Green Bowl\", \"style\": \"Italian\", \"address\": \"Veggie Street 15, Ramat-Gan\", \"open_hour\": \"08:00\", \"close_hour\": \"22:00\", \"vegetarian\": \"yes\", \"delivery\": \"yes\"}"
]`

### Terraform
1. Prerequisets: Install Azure CLI tool, Install Terrafom, Connect to Azure
1. Configure the Terraform Azure provider (main.tf)
    1. azurerm
1. Configure varibles (variables.tf, terraform.tfvars)
1. Create and add an Azure resource group (main.tf)
    1. Resource group
    1. Resources - plane, serviceapp, sql server, db, firewall
    1. Firewall - should restrict access to known IPs or Azure services
    1. SKU - plan & db - assume using tier "Standard" , size = "S1"
1. Configure outputs in main.tf
1. Deploy:
    1. `terraform init`
    1. `terraform plan`
    1. `terraform apply`
1. Check output:
    ```
    Apply complete! Resources: 6 added, 0 changed, 0 destroyed.

    Outputs:

    app_service_url = "my-restaurant-api.azurewebsites.net"
    sql_server_admin_login = "adminuser"
    sql_server_fqdn = "restaurant-sql-server.database.windows.net"
    sql_database_connection_string = <sensitive>
    ```

