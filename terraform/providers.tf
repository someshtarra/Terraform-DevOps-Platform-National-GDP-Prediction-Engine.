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
