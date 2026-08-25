output "vpc_id" {
  value       = aws_vpc.main.id
  description = "VPC ID"
}

output "eks_cluster_endpoint" {
  value       = aws_eks_cluster.main.endpoint
  description = "EKS Cluster API Endpoint"
}

output "eks_cluster_name" {
  value       = aws_eks_cluster.main.name
  description = "EKS Cluster Name"
}

output "ecr_repository_url" {
  value       = aws_ecr_repository.app.repository_url
  description = "AWS ECR Repository URL"
}

output "rds_endpoint" {
  value       = aws_db_instance.main.endpoint
  description = "RDS PostgreSQL Endpoint"
}

output "redis_endpoint" {
  value       = aws_elasticache_replication_group.redis.primary_endpoint_address
  description = "ElastiCache Redis Primary Endpoint"
}

output "s3_model_bucket" {
  value       = aws_s3_bucket.models.bucket
  description = "S3 Model Storage Bucket"
}

output "github_repository_url" {
  value       = github_repository.repo.html_url
  description = "GitHub Repository HTML URL"
}
