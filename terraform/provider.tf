terraform {
  required_version = ">= 1.7.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.50.0"
    }
    github = {
      source  = "integrations/github"
      version = "~> 6.2.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.30.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.13.0"
    }
  }

  backend "s3" {
    bucket         = "gdp-prediction-tf-state-bucket"
    key            = "environments/production/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "gdp-prediction-tf-locks"
    encrypt        = true
  }
}

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
  name       = aws_eks_cluster.main.name
  depends_on = [aws_eks_cluster.main]
}

data "aws_eks_cluster_auth" "cluster" {
  name       = aws_eks_cluster.main.name
  depends_on = [aws_eks_cluster.main]
}

provider "kubernetes" {
  host                   = aws_eks_cluster.main.endpoint
  cluster_ca_certificate = base64decode(aws_eks_cluster.main.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

provider "helm" {
  kubernetes {
    host                   = aws_eks_cluster.main.endpoint
    cluster_ca_certificate = base64decode(aws_eks_cluster.main.certificate_authority[0].data)
    token                  = data.aws_eks_cluster_auth.cluster.token
  }
}
