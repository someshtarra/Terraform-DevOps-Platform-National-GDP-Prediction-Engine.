resource "aws_secretsmanager_secret" "app_secrets" {
  name                    = "gdp-app-secrets-${var.environment}"
  recovery_window_in_days = var.environment == "production" ? 30 : 0

  tags = {
    Name = "gdp-app-secrets-${var.environment}"
  }
}

resource "aws_secretsmanager_secret_version" "app_secrets_val" {
  secret_id = aws_secretsmanager_secret.app_secrets.id
  secret_string = jsonencode({
    POSTGRES_USER     = "gdp_user"
    POSTGRES_PASSWORD = "ChangeMeInProduction123!"
    REDIS_PASSWORD    = "RedisSecureToken456!"
  })
}
