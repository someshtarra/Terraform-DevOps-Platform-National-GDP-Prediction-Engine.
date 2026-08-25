resource "kubernetes_deployment" "gdp_app" {
  metadata {
    name      = "gdp-prediction-app"
    namespace = kubernetes_namespace.app_ns.metadata[0].name
    labels = {
      app = "gdp-prediction-app"
    }
  }

  spec {
    replicas = var.environment == "production" ? 4 : 2

    selector {
      match_labels = {
        app = "gdp-prediction-app"
      }
    }

    strategy {
      type = "RollingUpdate"
      rolling_update {
        max_surge       = "25%"
        max_unavailable = "25%"
      }
    }

    template {
      metadata {
        labels = {
          app = "gdp-prediction-app"
        }
      }

      spec {
        service_account_name = kubernetes_service_account.app_sa.metadata[0].name

        security_context {
          run_as_non_root = true
          run_as_user     = 10001
          run_as_group    = 10001
          fs_group        = 10001
        }

        container {
          name  = "gdp-prediction-app"
          image = "${aws_ecr_repository.app.repository_url}:latest"

          security_context {
            allow_privilege_escalation = false
            read_only_root_filesystem  = true
            capabilities {
              drop = ["ALL"]
            }
          }

          port {
            container_port = 8000
          }

          env_from {
            config_map_ref {
              name = kubernetes_config_map.gdp_config.metadata[0].name
            }
          }

          resources {
            limits = {
              cpu    = "1000m"
              memory = "1024Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "512Mi"
            }
          }

          liveness_probe {
            http_get {
              path = "/health"
              port = 8000
            }
            initial_delay_seconds = 15
            period_seconds        = 10
          }

          readiness_probe {
            http_get {
              path = "/ready"
              port = 8000
            }
            initial_delay_seconds = 5
            period_seconds        = 5
          }
        }
      }
    }
  }

  depends_on = [aws_eks_node_group.main]
}
