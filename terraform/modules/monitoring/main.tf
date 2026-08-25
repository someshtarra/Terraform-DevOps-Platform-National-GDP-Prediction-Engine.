resource "aws_cloudwatch_log_group" "eks" {
  name              = "/aws/eks/${var.cluster_name}/cluster"
  retention_in_days = var.environment == "production" ? 90 : 14

  tags = {
    Name = "/aws/eks/${var.cluster_name}/cluster"
  }
}

resource "aws_cloudwatch_log_group" "app" {
  name              = "/aws/apps/gdp-prediction-${var.environment}"
  retention_in_days = var.environment == "production" ? 90 : 14

  tags = {
    Name = "/aws/apps/gdp-prediction-${var.environment}"
  }
}
