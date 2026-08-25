resource "kubernetes_namespace" "app_ns" {
  metadata {
    name = "gdp-${var.environment}"
    labels = {
      environment = var.environment
      managed-by  = "terraform"
    }
  }
}
