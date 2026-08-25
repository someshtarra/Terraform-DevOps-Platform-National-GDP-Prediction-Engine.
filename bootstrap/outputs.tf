output "state_bucket_name" {
  value       = aws_s3_bucket.terraform_state.bucket
  description = "S3 Remote State Bucket Name"
}

output "lock_table_name" {
  value       = aws_dynamodb_table.terraform_locks.name
  description = "DynamoDB State Locking Table Name"
}

output "kms_key_arn" {
  value       = aws_kms_key.terraform_state_key.arn
  description = "KMS Encryption Key ARN"
}
