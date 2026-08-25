module "network" {
  source       = "./modules/network"
  environment  = var.environment
  vpc_cidr     = var.vpc_cidr
  cluster_name = "${var.cluster_name}-${var.environment}"
}

module "iam" {
  source       = "./modules/iam"
  environment  = var.environment
  cluster_name = "${var.cluster_name}-${var.environment}"
}

module "container_registry" {
  source      = "./modules/container-registry"
  name        = "gdp-prediction-app"
  environment = var.environment
}

module "kubernetes" {
  source             = "./modules/kubernetes"
  cluster_name       = "${var.cluster_name}-${var.environment}"
  kubernetes_version = var.kubernetes_version
  environment        = var.environment
  vpc_id             = module.network.vpc_id
  subnet_ids         = module.network.private_subnet_ids
  cluster_role_arn   = module.iam.eks_cluster_role_arn
  node_role_arn      = module.iam.eks_node_role_arn
}

module "database" {
  source                = "./modules/database"
  environment           = var.environment
  vpc_id                = module.network.vpc_id
  subnet_ids            = module.network.database_subnet_ids
  eks_security_group_id = module.kubernetes.cluster_security_group_id
  instance_class        = var.db_instance_class
  db_name               = var.db_name
}

module "cache" {
  source                = "./modules/cache"
  environment           = var.environment
  vpc_id                = module.network.vpc_id
  subnet_ids            = module.network.database_subnet_ids
  eks_security_group_id = module.kubernetes.cluster_security_group_id
  node_type             = var.redis_node_type
}

module "storage" {
  source      = "./modules/storage"
  environment = var.environment
}

module "monitoring" {
  source       = "./modules/monitoring"
  environment  = var.environment
  cluster_name = "${var.cluster_name}-${var.environment}"
}
