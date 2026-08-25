resource "kubernetes_horizontal_pod_autoscaler_v2" "gdp_hpa" {
  metadata {
    name      = "gdp-prediction-hpa"
    namespace = kubernetes_namespace.app_ns.metadata[0].name
  }

  spec {
    min_replicas = var.environment == "production" ? 4 : 2
    max_replicas = var.environment == "production" ? 15 : 4

    scale_target_ref {
      api_version = "apps/v1"
      kind        = "Deployment"
      name        = kubernetes_deployment.gdp_app.metadata[0].name
    }

    metric {
      type = "Resource"
      resource {
        name = "cpu"
        target {
          type                = "Utilization"
          average_utilization = 75
        }
      }
    }
  }
}
