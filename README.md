# NimbusKart Cost Janitor

A FinOps-style cloud cost optimization and governance simulator built using Terraform, LocalStack, Python (boto3), and GitHub Actions.

---

# Overview

NimbusKart Cost Janitor identifies unused or non-compliant cloud resources in a simulated AWS environment and generates cost and compliance reports.

It focuses on detecting common cloud waste patterns and automating reporting during CI/CD runs.

---

# What this project does

The system scans and reports:

* Unattached EBS volumes
* Unassociated Elastic IPs (EIPs)
* Stopped EC2 instances
* Missing or incomplete resource tags

It generates:

* JSON report (`report.json`)
* Markdown summary (`summary.md`)
* GitHub PR comments (via CI)

---

# Key Judgements / Findings

## 1. Orphaned Storage (EBS Volumes)

### Observation

EBS volumes can remain unattached but still incur cost.

### Detection Logic

* Volume state = `available`

### Risk

* Silent cost leakage

### Prevention

* Auto-tag lifecycle policies
* Delete unattached volumes after threshold (e.g., 7–30 days)
* Enforce attachment via IaC (Terraform modules)

---

## 2. Orphaned Elastic IPs (EIPs)

### Observation

Elastic IPs not attached to instances still generate cost.

### Detection Logic

* No `InstanceId` associated

### Risk

* High recurring cost waste

### Prevention

* Auto-release unused EIPs
* Use NAT Gateway instead of multiple public IPs
* Enforce tagging + ownership

---

## 3. Stopped EC2 Instances

### Observation

Stopped instances still incur storage costs.

### Detection Logic

* Instance state = `stopped`
* Age threshold exceeded

### Risk

* Idle compute cost

### Prevention

* Auto-terminate after inactivity threshold
* Use auto-scaling groups instead of static instances

---

## 4. Missing / Incomplete Tags

### Observation

Some resources are created without required governance tags.

### Detection Logic

Required tags:

* Owner
* Project
* Environment
* Tier

### Risk

* No accountability
* No cost tracking
* Poor governance visibility

### Prevention

* Enforce tagging policies via:

  * Terraform validation
  * AWS Config rules
  * CI/CD checks (GitHub Actions)

---

# How to Avoid These Issues in Real Systems

## 1. Enforce Tag Policies Early

* Use Terraform `validation` rules
* Use OPA / Sentinel policies

---

## 2. Automate Cleanup

* Lambda-based janitor jobs
* Scheduled AWS EventBridge rules

---

## 3. CI/CD Governance

* Run scans on every Pull Request
* Block merges if orphan resources exceed threshold

---

## 4. Cost Monitoring

* Enable AWS Cost Explorer alerts
* Integrate CloudWatch billing alarms

---

## 5. Infrastructure Design Improvements

* Use Auto Scaling Groups
* Prefer managed services over raw EC2
* Use lifecycle policies for storage

---

# Basic Project Walkthrough

## Step 1: Start Local Environment

```bash
cd terraform
docker compose up -d
```

---

## Step 2: Provision Infrastructure

```bash
terraform init
terraform apply -auto-approve
```

---

## Step 3: Simulate Cost Waste

```bash
aws --endpoint-url=http://localhost:4566 ec2 allocate-address
```

---

## Step 4: Run Janitor

```bash
python janitor/janitor.py --dry-run
```

---

## Step 5: View Reports

* report.json → structured output
* summary.md → human-readable report

---

# CI/CD Automation

On every Pull Request:

* LocalStack starts
* Terraform provisions infra
* Orphan resources are created
* Janitor scans environment
* Reports are generated
* PR comment is posted with findings

---

# Project Structure Reference

See detailed setup and execution guide here:

👉 `docs/nimbuskart_cost_janitor_project_docs`

---

# Technologies Used

* Terraform
* Python (boto3)
* LocalStack
* Docker
* GitHub Actions
* AWS CLI

---

# Outcome

This project demonstrates real-world FinOps practices including:

* Cost leakage detection
* Infrastructure governance
* CI/CD automation
* Cloud resource lifecycle management

---

# Author

Chetan Patil
