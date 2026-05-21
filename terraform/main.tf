resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name        = "nimbuskart-vpc"
    Environment = "dev"
    Owner       = "engineering"
    Project     = "cost-optimization"
  }
}

resource "aws_s3_bucket" "app_bucket" {
  bucket = "nimbuskart-app-bucket"

  tags = {
    Name        = "nimbuskart-bucket"
    Environment = "dev"
    Owner       = "engineering"
    Project     = "cost-optimization"
  }
}
