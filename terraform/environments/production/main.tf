module "gdp_infrastructure" {
  source = "../../"

  aws_region         = var.aws_region
  environment        = var.environment
  vpc_cidr           = var.vpc_cidr
  cluster_name       = var.cluster_name
  kubernetes_version = var.kubernetes_version
  db_instance_class  = var.db_instance_class
  db_name            = var.db_name
  redis_node_type    = var.redis_node_type
}

variable "aws_region" {}
variable "environment" {}
variable "vpc_cidr" {}
variable "cluster_name" {}
variable "kubernetes_version" {}
variable "db_instance_class" {}
variable "db_name" {}
variable "redis_node_type" {}
