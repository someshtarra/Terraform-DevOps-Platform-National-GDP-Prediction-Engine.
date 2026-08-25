resource "kubernetes_network_policy_v1" "gdp_network_policy" {
  metadata {
    name      = "gdp-prediction-netpolicy"
    namespace = kubernetes_namespace.app_ns.metadata[0].name
  }

  spec {
    pod_selector {
      match_labels = {
        app = "gdp-prediction-app"
      }
    }

    ingress {
      from {
        namespace_selector {}
      }
      ports {
        protocol = "TCP"
        port     = 8000
      }
    }

    egress {
      to {
        ip_block {
          cidr = "0.0.0.0/0"
        }
      }
      ports {
        protocol = "TCP"
        port     = 5432
      }
      ports {
        protocol = "TCP"
        port     = 6379
      }
      ports {
        protocol = "TCP"
        port     = 443
      }
      ports {
        protocol = "UDP"
        port     = 53
      }
    }

    policy_types = ["Ingress", "Egress"]
  }
}
