output "latest_revision_fqdn" {
  value       = azurerm_container_app.example.latest_revision_fqdn
  description = "URL: The FQDN of the latest revision of the container app"
}