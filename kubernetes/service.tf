resource "kubernetes_service" "gdp_service" {
  metadata {
    name      = "gdp-prediction-service"
    namespace = kubernetes_namespace.app_ns.metadata[0].name
  }

  spec {
    selector = {
      app = "gdp-prediction-app"
    }

    port {
      port        = 8000
      target_port = 8000
    }

    type = "ClusterIP"
  }
}
