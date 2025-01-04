# Provider 
provider "azurerm" {
  features {}
  tenant_id     = var.tenant_id
  client_id     = var.client_id
  client_secret = var.client_secret
}

# Resources
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_app_service_plan" "appserviceplan" {
  name                = "restaurant-recommendation-appserviceplan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku {
    tier = var.app_service_plan_sku.tier
    size = var.app_service_plan_sku.size
  }
}

resource "azurerm_app_service" "appservice" {
  name                = "restaurant-recommendation-appservice"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  app_service_plan_id = azurerm_app_service_plan.appserviceplan.id
  app_settings = {
    DATABASE_URL = "Server=${azurerm_mssql_server.db_server.fully_qualified_domain_name};Database=${azurerm_sql_database.database.name};"
  }
}

resource "azurerm_mssql_server" "db_server" {
  name                         = "restaurant-sql-server"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"
  administrator_login          = var.sql_admin_username
  administrator_login_password = var.sql_admin_password
}


resource "azurerm_sql_database" "database" {
  name                = "restaurantdb"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_mssql_server.db_server.name
  sku {
    tier = "Standard"
    size = "S1"
  }
}

resource "azurerm_sql_firewall_rule" "allow_azure_services" {
  name                = "AllowAzureServices"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_mssql_server.db_server.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "0.0.0.0"
}

# Output 
output "app_service_url" {
  value = azurerm_app_service.app.default_site_hostname
}

output "sql_server_admin_login" {
  value = azurerm_mssql_server.db_server.administrator_login
}

output "sql_server_fqdn" {
  value = azurerm_mssql_server.db_server.fully_qualified_domain_name
}

output "sql_database_connection_string" {
  value = "Server=${azurerm_mssql_server.db_server.fully_qualified_domain_name};Database=${azurerm_sql_database.database.name};User Id=${azurerm_mssql_server.db_server.administrator_login};Password=${var.sql_admin_password};"
  sensitive = true
}