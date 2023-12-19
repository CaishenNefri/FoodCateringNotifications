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

import {
  to = azurerm_key_vault_access_policy.me
  id = "/subscriptions/1564f82f-9f08-47e0-9939-5e3dcc739b5e/resourceGroups/zdrowycatering/providers/Microsoft.KeyVault/vaults/kvzc/objectId/e3c0b5df-3a0d-4d56-b200-c44903c48bc9"
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
    "Restore",
    "Purge"
  ]
}

import {
  to = azurerm_key_vault_secret.telegram_token
  id = "https://kvzc.vault.azure.net/secrets/telegram-token/a437bde813324883a33852945bd79f16"
}

resource "azurerm_key_vault_secret" "telegram_token" {
  name         = "telegram-token"
  value        = var.telegram_token
  key_vault_id = azurerm_key_vault.example.id
}

import {
  to = azurerm_key_vault_secret.telegram_chat_id
  id = "https://kvzc.vault.azure.net/secrets/telegram-chat-id/e9822ce0fb014fe58874d58b687ed3ac"
}

resource "azurerm_key_vault_secret" "telegram_chat_id" {
  name         = "telegram-chat-id"
  value        = var.telegram_chat_id
  key_vault_id = azurerm_key_vault.example.id
}

import {
  to = azurerm_key_vault_secret.zc_username
  id = "https://kvzc.vault.azure.net/secrets/zc-username/1d7662de16d14f91a9fb0b6598982021"
}

resource "azurerm_key_vault_secret" "zc_username" {
  name         = "zc-username"
  value        = var.zc_username
  key_vault_id = azurerm_key_vault.example.id
}

import {
  to = azurerm_key_vault_secret.zc_password
  id = "https://kvzc.vault.azure.net/secrets/zc-password/cf131a75172f4081bfd9b05331ef7e46"
}

resource "azurerm_key_vault_secret" "zc_password" {
  name         = "zc-password"
  value        = var.zc_password
  key_vault_id = azurerm_key_vault.example.id
}