terraform {
  backend "s3" {
    bucket         = "gdp-prediction-tf-state-bucket"
    key            = "environments/global/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "gdp-prediction-tf-locks"
    encrypt        = true
  }
}
