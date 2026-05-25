# NimbusKart Cost Janitor

## Overview

NimbusKart Cost Janitor is a FinOps-inspired cloud governance and cost optimization project that detects unused or non-compliant AWS resources using Terraform, LocalStack, Python, and GitHub Actions.

The project simulates real-world cloud cost leak scenarios in a safe local environment using LocalStack and automatically generates reports for:

* Unattached EBS volumes
* Unassociated Elastic IPs (EIPs)
* Stopped EC2 instances
* Missing or non-compliant resource tags

The system also integrates with GitHub Actions to run automated infrastructure scans during Pull Requests.

---

# Architecture

## Components

### 1. Terraform

Terraform provisions cloud infrastructure resources in LocalStack.

Provisioned resources:

* VPC
* Public Subnets
* Security Groups
* EC2 Instances
* S3 Bucket
* EBS Volumes
* S3 Lifecycle Policies

---

### 2. LocalStack

LocalStack emulates AWS services locally.

Used services:

* EC2
* S3
* STS
* IAM

Purpose:

* Avoid AWS billing during development
* Enable local cloud testing
* Simulate orphaned resources safely

---

### 3. Python Janitor Engine

The janitor engine scans cloud resources using boto3.

Detection capabilities:

| Resource Type | Detection             |
| ------------- | --------------------- |
| EBS           | Unattached volumes    |
| Elastic IP    | Unassociated EIPs     |
| EC2           | Stopped instances     |
| EC2           | Missing required tags |

Generated outputs:

* `report.json`
* `summary.md`

---

### 4. GitHub Actions CI/CD

The project automatically runs infrastructure validation and cost scans during Pull Requests.

Pipeline responsibilities:

* Start LocalStack
* Initialize Terraform
* Provision infrastructure
* Simulate orphaned resources
* Run Janitor scans
* Upload reports as artifacts
* Comment findings on Pull Requests

---

# Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── cost-janitor.yml
│
├── janitor/
│   ├── janitor.py
│   ├── constants.py
│   └── requirements.txt
│
├── terraform/
│   ├── main.tf
│   ├── provider.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── modules/
│       └── network/
│
├── report.json
├── summary.md
└── README.md
```

---

# Prerequisites

Install the following:

* Docker
* Docker Compose Plugin
* Terraform >= 1.5
* Python >= 3.11
* AWS CLI
* Git

---

# Local Development Setup

## 1. Clone Repository

```bash
git clone https://github.com/chetan-patil7/NimbusKart-Cost-Optimisation.git
cd NimbusKart-Cost-Optimisation
```

---

## 2. Start LocalStack

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```

Expected:

```text
localstack/localstack
```

---

## 3. Setup Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r janitor/requirements.txt
```

---

## 4. Initialize Terraform

```bash
cd terraform
terraform init
```

---

## 5. Apply Infrastructure

```bash
terraform apply -auto-approve
```

---

# Simulating Cost Leaks

## Create Orphaned Elastic IP

```bash
aws --endpoint-url=http://localhost:4566 \
  ec2 allocate-address
```

---

## Create Untagged EC2 Instance

```bash
aws --endpoint-url=http://localhost:4566 \
  ec2 run-instances \
  --image-id ami-12345678 \
  --instance-type t2.micro
```

---

# Running the Janitor

## Dry Run Mode

```bash
python janitor/janitor.py --dry-run
```

Purpose:

* Detect resources
* Generate reports
* No deletion performed

---

## Delete Mode

```bash
python janitor/janitor.py --delete
```

Purpose:

* Detect resources
* Delete safe orphaned resources

---

# Sample Report

## JSON Output

```json
{
  "summary": {
    "total_orphans": 2,
    "estimated_monthly_waste_usd": 4.4
  }
}
```

---

## Markdown Summary

```md
# NimbusKart Cost Janitor Report

Total Findings: 2
Estimated Monthly Waste: $4.4

- ebs_volume (vol-xxxx): unattached
- elastic_ip (eipalloc-xxxx): unassociated
```

---

# GitHub Actions Workflow

The workflow runs automatically during Pull Requests.

Workflow file:

```text
.github/workflows/cost-janitor.yml
```

Pipeline stages:

1. Checkout repository
2. Setup Python
3. Install Terraform
4. Start LocalStack
5. Apply Terraform
6. Simulate orphan resources
7. Run Janitor scans
8. Upload reports
9. Comment PR summary

---

# Pull Request Workflow

Recommended Git workflow:

```bash
git checkout -b feature/cost-janitor
```

After making changes:

```bash
git add .
git commit -m "update janitor"
git push origin feature/cost-janitor
```

Then create a Pull Request to:

```text
main
```

---

# Security Considerations

Current implementation uses LocalStack test credentials:

```text
access_key=test
secret_key=test
```

Do not use these in production.

Recommended production improvements:

* IAM Roles
* OIDC authentication
* Secrets Manager
* GitHub Actions secrets

---

# Future Enhancements

Potential upgrades:

* Slack notifications
* Cost threshold alerts
* AWS Config style compliance engine
* Severity-based governance rules
* Automated remediation workflows
* Multi-account scanning
* CloudWatch integration
* Kubernetes cost analysis
* FinOps dashboards

---

# Learning Outcomes

This project demonstrates:

* Infrastructure as Code (Terraform)
* Local AWS emulation using LocalStack
* FinOps concepts
* Cloud governance automation
* boto3 automation
* GitHub Actions CI/CD
* Pull Request automation
* Resource lifecycle management
* Cost optimization principles

---

# Technologies Used

| Technology     | Purpose                     |
| -------------- | --------------------------- |
| Terraform      | Infrastructure provisioning |
| Python         | Janitor automation          |
| boto3          | AWS SDK                     |
| LocalStack     | AWS emulation               |
| Docker         | Container runtime           |
| GitHub Actions | CI/CD                       |
| AWS CLI        | Resource management         |

---

# Author

Chetan Patil

GitHub Repository:

[https://github.com/chetan-patil7/NimbusKart-Cost-Optimisation](https://github.com/chetan-patil7/NimbusKart-Cost-Optimisation)