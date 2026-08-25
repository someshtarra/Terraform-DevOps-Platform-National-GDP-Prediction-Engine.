resource "kubernetes_service_account" "app_sa" {
  metadata {
    name      = "gdp-app-sa"
    namespace = kubernetes_namespace.app_ns.metadata[0].name
    annotations = {
      "eks.amazonaws.com/role-arn" = aws_iam_role.eks_node_role.arn
    }
  }
}
