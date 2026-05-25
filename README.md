# NimbusKart Cost Janitor

## Overview

NimbusKart Cost Janitor is a FinOps simulation project that detects unused and non-compliant cloud resources in a safe LocalStack environment. It automates infrastructure provisioning with Terraform, scans for cost leaks using a Python-based janitor, and integrates with GitHub Actions to validate cloud hygiene during pull requests.

## How to run locally

````bash
# Clone repository
git clone https://github.com/chetan-patil7/NimbusKart-Cost-Optimisation.git
cd NimbusKart-Cost-Optimisation

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r janitor/requirements.txt

# Start LocalStack
docker compose up -d

# Initialize Terraform
cd terraform
terraform init
terraform apply -auto-approve

# Go back to root
cd ..

# Create sample orphan resource
aws --endpoint-url=http://localhost:4566 ec2 allocate-address

# Run janitor
python janitor/janitor.py --dry-run
```bash
# Clone repository
git clone https://github.com/chetan-patil7/NimbusKart-Cost-Optimisation.git
cd NimbusKart-Cost-Optimisation

# Start LocalStack
docker compose up -d

# Initialize Terraform
cd terraform
terraform init
terraform apply -auto-approve

# Go back to root
cd ..

# Create sample orphan resource
aws --endpoint-url=http://localhost:4566 ec2 allocate-address

# Run janitor
python janitor/janitor.py --dry-run
````

## Architecture

```
+-------------------+        +------------------+
|   GitHub Actions  | -----> |   LocalStack     |
| (CI/CD Pipeline)  |        | (AWS Emulator)   |
+-------------------+        +------------------+
           |                          |
           v                          v
+-------------------+        +------------------+
|   Terraform       | -----> | AWS Resources     |
| (IaC Provisioning)|        | EC2 / EBS / EIP   |
+-------------------+        +------------------+
           |
           v
+-------------------+
| Python Janitor    |
| (Cost Scanner)    |
+-------------------+
           |
           v
+-------------------+
| Reports           |
| report.json       |
| summary.md        |
+-------------------+
```

## Decisions & deviations

* Used LocalStack instead of real AWS to avoid cloud costs during development
* Used Terraform provider endpoint overrides for local AWS simulation
* Implemented tag-based governance using a static REQUIRED_TAGS policy
* Chose GitHub Actions artifacts instead of committing generated reports to repository
* Used PR-based CI execution instead of direct main branch execution
* Added manual simulation of orphan resources for testing cost leakage scenarios

## Trade-offs

* Did not integrate real AWS accounts due to cost and security constraints
* No persistent database for scan history (currently file-based reporting only)
* No centralized dashboard (reports are static JSON/Markdown outputs)
* Limited scaling design (single-run batch scanner instead of continuous monitoring)
* No advanced policy engine (like OPA or AWS Config) implemented yet

## AI usage disclosure

This project was developed with assistance from an AI coding assistant to help with:

* Debugging Terraform and LocalStack configuration issues
* Designing Python-based resource scanning logic
* Structuring GitHub Actions CI/CD workflow
* Improving documentation clarity and formatting

All final decisions, implementation, and validation were reviewed and applied manually by the developer.