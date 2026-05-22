variable "aws_region" {
  default = "us-east-1"
}

variable "environment" {
  default = "staging"
}

variable "project" {
  default = "NimbusKart"
}

variable "owner" {
  default = "platform-team"
}

variable "ssh_allowed_cidr" {
  description = "CIDR allowed for SSH access"
  default     = "0.0.0.0/0"
}

variable "instance_type" {
  default = "t3.micro"
}
