/*
 * DEMONSTRATION ONLY - NOT FOR PRODUCTION USE
 * This Terraform configuration is for educational purposes only.
 * The S3 bucket name is an example and may not be available.
 * No actual infrastructure should be deployed from this configuration.
 */

provider "aws" {
  region = "eu-west-2" # London region
}

terraform {
  backend "s3" {
    bucket = "devsecops-project-bucket"
    key    = "global/s3/terraform.tfstate"
    region = "eu-west-2"
  }
}

resource "aws_s3_bucket" "devsecops-project-bucket" {
  bucket = "devsecops-project-bucket"
}

# REMEDIATED: Block all public access to the S3 bucket to fix AVD-AWS-0086, AVD-AWS-0087, AVD-AWS-0091, AVD-AWS-0093
resource "aws_s3_bucket_public_access_block" "devsecops_bucket_pab" {
  bucket = aws_s3_bucket.devsecops-project-bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# REMEDIATED: Enable server-side encryption by default to fix AVD-AWS-0088 and AVD-AWS-0132
resource "aws_s3_bucket_server_side_encryption_configuration" "devsecops_bucket_sse" {
  bucket = aws_s3_bucket.devsecops-project-bucket.id

  rule {
    apply_server_side_encryption_by_default {
      # Using AWS-managed keys is a strong security baseline.
      # A customer-managed key (CMK) could be used for even greater control.
      sse_algorithm = "AES256"
    }
  }
}