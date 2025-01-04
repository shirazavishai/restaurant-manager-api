variable "tenant_id" {
  description = "The Tenant ID for Azure"
  type        = string
}

variable "client_id" {
  description = "The Client ID for Azure"
  type        = string
}

variable "client_secret" {
  description = "The Client Secret for Azure"
  type        = string
  sensitive   = true 
}

variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
  default     = "restaurant-recommendation-api-resources"
}

variable "location" {
  description = "The location of the resources"
  type        = string
  default     = "West Europe"
}

variable "sql_admin_username" {
  description = "The administrator username for SQL Server"
  type        = string
  default     = "sqladmin"
}

variable "sql_admin_password" {
  description = "The administrator password for SQL Server"
  type        = string
  sensitive   = true 
}

variable "app_service_plan_sku" {
  type = object({
    tier = string
    size = string
  })
  default = {
    tier = "Standard"
    size = "S1"
  }
}