output "namespace" {
  value = kubernetes_namespace.app_ns.metadata[0].name
}

output "service_name" {
  value = kubernetes_service.gdp_service.metadata[0].name
}
