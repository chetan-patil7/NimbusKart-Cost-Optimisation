# NimbusKart Cost Optimization Platform

Infrastructure cost optimization and orphan resource detection platform built using:

- Terraform
- LocalStack
- Python
- GitHub Actions

## Features

### Infrastructure as Code
- VPC with public subnets
- Security groups
- EC2 web tier
- S3 logging bucket
- Lifecycle rules
- Orphan EBS volume simulation

### Cost Janitor
Detects:
- Unattached EBS volumes
- Stopped EC2 instances
- Unused Elastic IPs
- Missing required tags

Supports:
- Dry-run mode
- Delete mode
- Protected=true safeguard
- JSON + Markdown reporting

### CI/CD
GitHub Actions workflow:
- Spins up LocalStack
- Applies Terraform
- Runs Janitor
- Uploads reports
- Comments findings on PRs

---

## Local Setup

### Start LocalStack

```bash
docker compose up -d
```

### Terraform

```bash
cd terraform

terraform init
terraform fmt -recursive
terraform validate
terraform apply -auto-approve
```

### Run Janitor

```bash
python janitor/janitor.py --dry-run
```

---

## Repository Structure

```text
terraform/   -> Infrastructure as Code
janitor/     -> Cost detection automation
.github/     -> CI/CD workflows
docs/        -> Walkthrough & documentation
samples/     -> Example reports
```
