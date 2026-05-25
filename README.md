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

- Allowed SSH access from `0.0.0.0/0` only to match the assignment requirement; this is unsafe for production and should normally be restricted to trusted IP ranges or VPN access.

- Used LocalStack instead of a real AWS account to ensure the entire project remains free, reproducible, and safe for testing.

- Added common Terraform tags through reusable locals/variables to guarantee all supported resources consistently receive mandatory tags.

- Kept the infrastructure in a single AWS region (`us-east-1`) because multi-region support was outside the assignment scope.

- Used static monthly pricing estimates for orphaned resources because LocalStack does not provide real AWS billing data.

- Implemented the Janitor in Python instead of Bash for better structure, extensibility, JSON handling, and testability.

- The `--dry-run` mode is enabled by default to prioritize safety and prevent accidental deletions.

- Resources tagged with `Protected=true` are skipped even in `--delete` mode to reduce the risk of destructive automation mistakes.

- The intentionally unattached EBS volume was preserved because the assignment explicitly requires a known orphan resource for testing the Janitor workflow.

- Used modular Terraform structure (`modules/network`) instead of a flat configuration to improve maintainability and reusability.

- Lifecycle cleanup was implemented only for non-current S3 object versions after 30 days, as requested by the specification.

- The GitHub Actions workflow fails intentionally when orphaned resources are detected in `--dry-run` mode so that cost issues are visible during pull request reviews.

- Assumed LocalStack feature compatibility for EC2, S3, EBS, and networking resources because some AWS services behave differently in emulated environments.

- Did not implement automatic remediation approvals or notification integrations (Slack/Email) to keep the scope aligned with the assignment time budget.

- Chose not to auto-delete stopped EC2 instances by default because stopped instances may still contain important data or attached volumes.

- Used Terraform variables with defaults instead of hardcoding environment values to make the setup reusable across environments.

- Treated missing mandatory tags as a cost hygiene issue because untagged resources cannot be reliably attributed to teams or projects.
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
