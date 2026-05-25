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

<img width="1536" height="1024" alt="NimbusKart Architecture" src="https://github.com/user-attachments/assets/276967f7-3bb5-4020-b955-fdc183899736" />

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

## AI Usage Disclosure

This project was built using ChatGPT.

### Usage
- Used for Terraform architecture design and module structure
- Helped implement Cost Janitor logic (orphan detection + reporting)
- Assisted in GitHub Actions CI/CD workflow setup
- Helped write DESIGN.md and documentation

### Issue Found
ChatGPT suggested using `http://localstack:4566` for CI, which failed in GitHub Actions.  
It was corrected to `http://localhost:4566` after testing.

### Manual Work
CI/CD workflow debugging and fixing LocalStack execution timing was done manually due to environment-specific behavior.

All final decisions, implementation, and validation were reviewed and applied manually by myself.
