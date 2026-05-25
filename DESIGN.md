## 1. Multi-Cloud Design (AWS → GCP → Azure)

The current Janitor is designed around AWS SDK calls (boto3). To support multiple cloud providers without rewriting the core logic, the system must be split into **three clear layers**:


### Proposed Architecture

<img width="1536" height="1024" alt="NimbusKart Architecture" src="https://github.com/user-attachments/assets/6d2cf6cf-cd2c-4ee1-9fc5-3832d091d253" />


### Key Idea: Normalized Resource Model

Every provider MUST convert resources into a common structure:

```json
{
  "resource_id": "string",
  "resource_type": "ebs_volume | vm | ip | snapshot",
  "region": "string",
  "state": "string",
  "tags": {},
  "created_at": "timestamp",
  "cost_per_month": "float"
}
````

### Why this works

* Core engine never calls AWS/GCP/Azure directly
* Only provider adapters change per cloud
* Policy engine remains unchanged across clouds
* Enables scaling to multi-account + multi-cloud FinOps

---

## 2. IAM Permissions

### Dry-run mode (read-only)

Janitor only inspects resources. It must NOT modify anything.

Required permissions:

* ec2:DescribeInstances
* ec2:DescribeVolumes
* ec2:DescribeAddresses
* ec2:DescribeSnapshots
* ec2:DescribeTags
* s3:ListAllMyBuckets
* s3:GetBucketTagging

### Minimal Read-Only IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadOnlyCostJanitor",
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeVolumes",
        "ec2:DescribeAddresses",
        "ec2:DescribeSnapshots",
        "ec2:DescribeTags",
        "s3:ListAllMyBuckets",
        "s3:GetBucketTagging"
      ],
      "Resource": "*"
    }
  ]
}
```

### Delete mode (additional permissions)

Only enabled in explicit execution mode:

* ec2:TerminateInstances
* ec2:DeleteVolume
* ec2:ReleaseAddress
* s3:DeleteObject (future extension)

---

## 3. Safety Nets (Failure Modes)

### Failure Mode 1: Deleting "stopped but critical" recovery instances

Problem:
Some stopped EC2 instances are intentionally kept for:

* disaster recovery
* debugging production incidents
* batch job reruns

Naïve deletion would remove recovery capability.

Guardrails:

* Require tag: `Protected=true`
* Add minimum age threshold for deletion eligibility
* Require instance classification tag: `Tier != "critical"`
* Introduce quarantine mode before deletion (mark → wait → delete)

---

### Failure Mode 2: Deleting unattached EBS volumes that contain backups

Problem:
Not all unattached volumes are waste. Some are:

* manual snapshots
* backup staging disks
* forensic investigation data

Guardrails:

* Snapshot volume before deletion
* Check tag: `Backup=true` → never delete
* Introduce retention window (e.g., 7–30 days)
* Require owner confirmation for large volumes (>100GB)

---

## 4. Observability Strategy

The goal is to measure:

* waste detection efficiency
* execution reliability
* cost impact

### Metrics

#### 1. orphan_resources_total

* Source: Janitor scan output
* Alert threshold: > 20
* Meaning: excessive waste detected

#### 2. estimated_monthly_waste_usd

* Source: report.json aggregation
* Alert threshold: > 500 USD
* Meaning: cost inefficiency spike

#### 3. janitor_scan_duration_seconds

* Source: CI workflow runtime
* Alert threshold: > 300 seconds
* Meaning: scalability issue or API bottleneck

#### 4. deletion_failures_total

* Source: delete mode execution logs
* Alert threshold: > 0
* Meaning: partial cleanup failure

#### 5. untagged_resources_total

* Source: tag validation scanner
* Alert threshold: > 10
* Meaning: governance violation trend

### Where to publish

* AWS CloudWatch (primary in AWS setup)
* Prometheus + Grafana (multi-cloud expansion)
* Slack webhook alerts (FinOps notifications)

---

## 5. What Was NOT Built (Scope Decisions)

This implementation intentionally avoids production-grade complexity such as:

* Distributed scheduling (Airflow / EventBridge / Kubernetes CronJobs)
* Multi-account AWS Organizations integration
* Real billing data ingestion (CUR reports, Cost Explorer API)
* Machine learning-based waste prediction
* Automated approval workflows for deletions
* Role-based access control dashboards

The system is designed as a **safe, local-first FinOps simulation platform**, focusing on:

* Infrastructure as Code correctness
* Orphan resource detection logic
* CI/CD integration
* Safety-first deletion design patterns

Production systems would extend this with real billing pipelines, multi-account governance, and approval-based remediation workflows.

```
```
