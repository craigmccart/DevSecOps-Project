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