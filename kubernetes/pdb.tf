resource "kubernetes_pod_disruption_budget_v1" "gdp_pdb" {
  metadata {
    name      = "gdp-prediction-pdb"
    namespace = kubernetes_namespace.app_ns.metadata[0].name
  }

  spec {
    min_available = var.environment == "production" ? 2 : 1

    selector {
      match_labels = {
        app = "gdp-prediction-app"
      }
    }
  }
}
