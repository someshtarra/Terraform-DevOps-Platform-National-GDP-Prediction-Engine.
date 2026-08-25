output "bucket_name" {
  value = aws_s3_bucket.models.bucket
}

output "bucket_arn" {
  value = aws_s3_bucket.models.arn
}
