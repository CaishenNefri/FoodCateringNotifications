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


resource "azurerm_key_vault_secret" "telegram_token" {
  name         = "telegram-token"
  value        = var.telegram_token
  key_vault_id = azurerm_key_vault.example.id
}

resource "azurerm_key_vault_secret" "telegram_chat_id" {
  name         = "telegram-chat-id"
  value        = var.telegram_chat_id
  key_vault_id = azurerm_key_vault.example.id
}

resource "azurerm_key_vault_secret" "zc_username" {
  name         = "zc-username"
  value        = var.zc_username
  key_vault_id = azurerm_key_vault.example.id
}

resource "azurerm_key_vault_secret" "zc_password" {
  name         = "zc-password"
  value        = var.zc_password
  key_vault_id = azurerm_key_vault.example.id
}

resource "azurerm_key_vault_secret" "container_app_fqdn" {
  name         = "container-app-fqdn"
  value        = azurerm_container_app.example.latest_revision_fqdn
  key_vault_id = azurerm_key_vault.example.id
}