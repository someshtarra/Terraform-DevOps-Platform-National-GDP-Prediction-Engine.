resource "kubernetes_ingress_v1" "gdp_ingress" {
  metadata {
    name      = "gdp-prediction-ingress"
    namespace = kubernetes_namespace.app_ns.metadata[0].name
    annotations = {
      "kubernetes.io/ingress.class"               = "alb"
      "alb.ingress.kubernetes.io/scheme"          = "internet-facing"
      "alb.ingress.kubernetes.io/target-type"     = "ip"
      "alb.ingress.kubernetes.io/certificate-arn" = aws_acm_certificate.cert.arn
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
