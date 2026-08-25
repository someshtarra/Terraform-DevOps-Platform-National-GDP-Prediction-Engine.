resource "kubernetes_config_map" "gdp_config" {
  metadata {
    name      = "gdp-prediction-config"
    namespace = kubernetes_namespace.app_ns.metadata[0].name
  }

  data = {
    APP_ENV       = var.environment
    POSTGRES_HOST = aws_db_instance.main.address
    POSTGRES_PORT = "5432"
    POSTGRES_DB   = var.db_name
    REDIS_HOST    = aws_elasticache_replication_group.redis.primary_endpoint_address
    REDIS_PORT    = "6379"
  }
}
