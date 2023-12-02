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

# Container App
resource "azurerm_container_app_environment" "example" {
  name                = "Example-Environment"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
}
resource "azurerm_container_app" "example" {
  name                         = "example-app"
  container_app_environment_id = azurerm_container_app_environment.example.id
  resource_group_name          = azurerm_resource_group.example.name
  revision_mode                = "Multiple"

  identity {
    type = "UserAssigned"
    identity_ids = [
      azurerm_user_assigned_identity.example.id
    ]
  }

  ingress {
    allow_insecure_connections = true
    external_enabled           = true
    target_port                = 4444
    # exposed_port = 4444
    # transport = "auto"
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  template {
    min_replicas = 1
    max_replicas = 1
    container {
      name   = "browser-chrome"
      image  = "selenium/standalone-chrome"
      cpu    = 1
      memory = "2Gi"

      readiness_probe {
        # path                    = "/readyz"
        path                    = "/wd/hub/status"
        port                    = 4444
        transport               = "HTTP"
        failure_count_threshold = 1
        timeout                 = 5

      }

      liveness_probe {
        # path                    = "/readyz"
        path                    = "/wd/hub/status"
        port                    = 4444
        failure_count_threshold = 1
        transport               = "HTTP"
        timeout                 = 5
        initial_delay           = 12
      }

      # startup_probe {
      #   path      = "/wd/hub/status"
      #   port      = 4444
      #   transport = "HTTP"
      #   timeout   = 240
      # }
    }
  }
}