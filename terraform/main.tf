provider "aws" {
  region     = "specify-region"
  access_key = "your-access-key"
  secret_key = "your-secret-key"
}

resource "aws_s3_bucket" "remediate" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_server_side_encryption_configuration" "example" {
  bucket = aws_s3_bucket.remediate.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm      = "aws:kms"
      kms_master_key_id  = "your-kms-key-id"
    }
  }
}
