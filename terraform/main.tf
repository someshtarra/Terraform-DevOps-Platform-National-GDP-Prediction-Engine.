# ------------------------------------------------------------------------------
# 1. AWS CLOUD PROVIDER INFRASTRUCTURE
# ------------------------------------------------------------------------------
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

module "secrets_manager" {
  source      = "./modules/secrets-manager"
  environment = var.environment
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

module "dns" {
  source      = "./modules/dns"
  domain_name = var.domain_name
}

# ------------------------------------------------------------------------------
# 2. GITHUB PROVIDER INFRASTRUCTURE
# ------------------------------------------------------------------------------
module "github" {
  source          = "./modules/github"
  repository_name = "TERRAFORM"
}

# ------------------------------------------------------------------------------
# 3. KUBERNETES PROVIDER WORKLOADS
# ------------------------------------------------------------------------------
module "k8s_workloads" {
  source              = "./modules/k8s-workloads"
  environment         = var.environment
  ecr_repository_url  = module.container_registry.repository_url
  domain_name         = var.domain_name
  acm_certificate_arn = module.dns.certificate_arn

  depends_on = [module.kubernetes]
}
