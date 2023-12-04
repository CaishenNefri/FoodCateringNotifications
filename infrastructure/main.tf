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

resource "azurerm_log_analytics_workspace" "example" {
  name                = "acctest-02"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

# Container App
resource "azurerm_container_app_environment" "example" {
  name                       = "Example-Environment2"
  location                   = azurerm_resource_group.example.location
  resource_group_name        = azurerm_resource_group.example.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.example.id
}
