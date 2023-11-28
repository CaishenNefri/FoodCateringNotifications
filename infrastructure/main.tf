# Resource group
resource "azurerm_resource_group" "example" {
  name     = "zdrowycatering"
  location = "West Europe"
}


# User Managed Identity
resource "azurerm_user_assigned_identity" "example" {
  name                = "identity"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
}


resource "azurerm_key_vault" "example" {
  name                        = "kvzc"
  resource_group_name         = azurerm_resource_group.example.name
  location                    = azurerm_resource_group.example.location
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "standard"
}

resource "azurerm_key_vault_access_policy" "identity" {
  key_vault_id = azurerm_key_vault.example.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azurerm_user_assigned_identity.example.principal_id

  key_permissions = [
    "Get",
    "List",
    "Create",
    "Delete",
    "Backup",
    "Restore"
  ]

  secret_permissions = [
    "Get",
    "List",
    "Set",
    "Delete",
    "Backup",
    "Restore"
  ]
}


resource "azurerm_key_vault_access_policy" "me" {
  key_vault_id = azurerm_key_vault.example.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azurerm_client_config.current.object_id

  key_permissions = [
    "Get",
    "List",
    "Create",
    "Delete",
    "Backup",
    "Restore"
  ]

  secret_permissions = [
    "Get",
    "List",
    "Set",
    "Delete",
    "Backup",
    "Restore"
  ]
}



# Container App
# resource "azurerm_container_app_environment" "example" {
#   name                = "Example-Environment"
#   location            = azurerm_resource_group.example.location
#   resource_group_name = azurerm_resource_group.example.name
# }
# resource "azurerm_container_app" "example" {
#   name                         = "example-app"
#   container_app_environment_id = azurerm_container_app_environment.example.id
#   resource_group_name          = azurerm_resource_group.example.name
#   revision_mode                = "Multiple"

#   identity {
#     type = "UserAssigned"
#     identity_ids = [
#       azurerm_user_assigned_identity.example.id
#     ]
#   }

#   ingress {
#     allow_insecure_connections = true
#     external_enabled           = true
#     target_port                = 4444
#     # exposed_port = 4444
#     # transport = "auto"
#     traffic_weight {
#       percentage = 100
#     }
#   }

#   template {
#     container {
#       name   = "browser-chrome"
#       image  = "selenium/standalone-chrome"
#       cpu    = 0.25
#       memory = "0.5Gi"
#     }
#   }
# }