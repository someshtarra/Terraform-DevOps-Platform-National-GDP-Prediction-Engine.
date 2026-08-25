variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "Target AWS Region"
}

variable "state_bucket_name" {
  type        = string
  default     = "gdp-prediction-tf-state-bucket"
  description = "Name of S3 bucket for Terraform remote state"
}

variable "lock_table_name" {
  type        = string
  default     = "gdp-prediction-tf-locks"
  description = "Name of DynamoDB table for Terraform state locking"
}
