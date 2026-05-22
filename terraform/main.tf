module "network" {
  source = "./modules/network"

  vpc_cidr             = "10.20.0.0/16"
  public_subnet_1_cidr = "10.20.1.0/24"
  public_subnet_2_cidr = "10.20.2.0/24"

  environment = var.environment
  project     = var.project
  owner       = var.owner
}

resource "aws_security_group" "web_sg" {
  name   = "web-sg"
  vpc_id = module.network.vpc_id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH - WARNING open to world by default"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_allowed_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "web-sg"
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}

resource "aws_instance" "web_1" {
  ami                    = "ami-12345678"
  instance_type          = var.instance_type
  subnet_id              = module.network.public_subnet_1_id
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tags = {
    Name        = "web-1"
    Tier        = "web"
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}

resource "aws_instance" "web_2" {
  ami                    = "ami-12345678"
  instance_type          = var.instance_type
  subnet_id              = module.network.public_subnet_2_id
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tags = {
    Name        = "web-2"
    Tier        = "web"
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}

resource "aws_s3_bucket" "logs_bucket" {
  bucket = "nimbuskart-staging-logs"

  tags = {
    Name        = "logs-bucket"
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.logs_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "lifecycle" {
  bucket = aws_s3_bucket.logs_bucket.id

  rule {
    id     = "expire-old-versions"
    status = "Enabled"

    filter {
      prefix = "" # applies to entire bucket
    }

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}

resource "aws_ebs_volume" "orphan_volume" {
  availability_zone = "us-east-1a"
  size              = 10

  tags = {
    Name        = "orphan-ebs-volume"
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}
