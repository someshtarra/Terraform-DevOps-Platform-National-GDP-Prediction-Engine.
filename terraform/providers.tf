provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "National-GDP-Prediction"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Repository  = "https://github.com/someshtarra/TERRAFORM"
    }
  }
}

provider "github" {
  owner = var.github_owner
  token = var.github_token
}

data "aws_eks_cluster" "cluster" {
  name = module.kubernetes.cluster_name
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.kubernetes.cluster_name
}

provider "kubernetes" {
  host                   = module.kubernetes.cluster_endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

provider "helm" {
  kubernetes {
    host                   = module.kubernetes.cluster_endpoint
    cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority[0].data)
    token                  = data.aws_eks_cluster_auth.cluster.token
  }
}
