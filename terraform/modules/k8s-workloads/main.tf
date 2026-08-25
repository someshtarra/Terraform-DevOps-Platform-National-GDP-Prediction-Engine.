resource "kubernetes_namespace" "app_ns" {
  metadata {
    name = "gdp-${var.environment}"
    labels = {
      environment = var.environment
      managed-by  = "terraform"
    }
  }
}

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

    template {
      metadata {
        labels = {
          app = "gdp-prediction-app"
        }
      }

      spec {
        container {
          name  = "gdp-prediction-app"
          image = "${var.ecr_repository_url}:latest"

          port {
            container_port = 8000
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
}

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

resource "kubernetes_ingress_v1" "gdp_ingress" {
  metadata {
    name      = "gdp-prediction-ingress"
    namespace = kubernetes_namespace.app_ns.metadata[0].name
    annotations = {
      "kubernetes.io/ingress.class"               = "alb"
      "alb.ingress.kubernetes.io/scheme"          = "internet-facing"
      "alb.ingress.kubernetes.io/target-type"     = "ip"
      "alb.ingress.kubernetes.io/certificate-arn" = var.acm_certificate_arn
    }
  }

  spec {
    rule {
      host = var.domain_name
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.gdp_service.metadata[0].name
              port {
                number = 8000
              }
            }
          }
        }
      }
    }
  }
}

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
