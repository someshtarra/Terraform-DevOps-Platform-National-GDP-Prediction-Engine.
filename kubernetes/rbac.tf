resource "kubernetes_role" "app_role" {
  metadata {
    name      = "gdp-app-role"
    namespace = kubernetes_namespace.app_ns.metadata[0].name
  }

  rule {
    api_groups = [""]
    resources  = ["configmaps", "secrets"]
    verbs      = ["get", "list"]
  }
}

resource "kubernetes_role_binding" "app_rolebinding" {
  metadata {
    name      = "gdp-app-rolebinding"
    namespace = kubernetes_namespace.app_ns.metadata[0].name
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "Role"
    name      = kubernetes_role.app_role.metadata[0].name
  }

  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.app_sa.metadata[0].name
    namespace = kubernetes_namespace.app_ns.metadata[0].name
  }
}
