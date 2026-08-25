variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "Target AWS Region"
}

variable "environment" {
  type        = string
  default     = "dev"
  description = "Environment name (dev, staging, production)"
}

variable "vpc_cidr" {
  type        = string
  default     = "10.0.0.0/16"
  description = "VPC CIDR Block"
}

variable "cluster_name" {
  type        = string
  default     = "gdp-prediction-eks"
  description = "AWS EKS Cluster Name"
}

variable "kubernetes_version" {
  type        = string
  default     = "1.30"
  description = "Kubernetes Version"
}

variable "db_instance_class" {
  type        = string
  default     = "db.t4g.medium"
  description = "RDS PostgreSQL Instance Class"
}

variable "db_name" {
  type        = string
  default     = "gdp_db"
  description = "RDS Database Name"
}

variable "redis_node_type" {
  type        = string
  default     = "cache.t4g.micro"
  description = "ElastiCache Redis Node Type"
}

variable "github_owner" {
  type        = string
  default     = "someshtarra"
  description = "GitHub Repository Owner / Organization"
}

variable "github_token" {
  type        = string
  default     = ""
  sensitive   = true
  description = "GitHub Personal Access Token for GitHub Provider"
}

variable "domain_name" {
  type        = string
  default     = "gdp.api.domain.com"
  description = "Domain name for Route 53 and ACM Certificate"
}
