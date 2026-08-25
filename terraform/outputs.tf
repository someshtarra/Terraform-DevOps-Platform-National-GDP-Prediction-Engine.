output "vpc_id" {
  value       = module.network.vpc_id
  description = "VPC ID"
}

output "eks_cluster_endpoint" {
  value       = module.kubernetes.cluster_endpoint
  description = "EKS Cluster API Endpoint"
}

output "eks_cluster_name" {
  value       = module.kubernetes.cluster_name
  description = "EKS Cluster Name"
}

output "ecr_repository_url" {
  value       = module.container_registry.repository_url
  description = "AWS ECR Repository URL"
}

output "rds_endpoint" {
  value       = module.database.rds_endpoint
  description = "RDS PostgreSQL Endpoint"
}

output "redis_endpoint" {
  value       = module.cache.redis_endpoint
  description = "ElastiCache Redis Primary Endpoint"
}

output "s3_model_bucket" {
  value       = module.storage.bucket_name
  description = "S3 Model Storage Bucket"
}
