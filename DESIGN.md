# DESIGN.md

## 1. Multi-Cloud Architecture

To support AWS, GCP, and Azure without rewriting the core logic, the Janitor should follow a provider abstraction model.

### Proposed Structure

```text
janitor/
├── core/
│   ├── scanner.py
│   ├── reporter.py
│   └── policies.py
│
├── providers/
│   ├── aws/
│   ├── gcp/
│   └── azure/
```

### Responsibilities

- core/scanner.py
  - Executes scan workflow
  - Aggregates findings
  - Applies deletion policies

- providers/aws/
  - AWS-specific SDK calls
  - Maps resources into normalized schema

- providers/gcp/
  - Uses Google Cloud SDK
  - Returns normalized findings

- providers/azure/
  - Uses Azure SDK
  - Returns normalized findings

### Normalized Resource Model

Each provider returns:

```json
{
  "resource_id": "",
  "resource_type": "",
  "region": "",
  "tags": {}
}
```

This allows the core engine to remain cloud-agnostic.

---

## 2. IAM Permissions

### Dry Run Mode

Requires read-only permissions:
- ec2:DescribeInstances
- ec2:DescribeVolumes
- ec2:DescribeAddresses
- ec2:DescribeSnapshots
- s3:ListBucket
- s3:GetBucketTagging

### Delete Mode

Additional permissions:
- ec2:DeleteVolume
- ec2:TerminateInstances
- ec2:ReleaseAddress

### Minimal Read-Only IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeVolumes",
        "ec2:DescribeAddresses",
        "ec2:DescribeSnapshots",
        "s3:ListBucket",
        "s3:GetBucketTagging"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## 3. Safety Net

### Failure Mode 1
Deleting a stopped EC2 instance used for disaster recovery.

### Guardrail
- Require minimum age threshold
- Require approval workflow before deletion
- Skip Protected=true resources

---

### Failure Mode 2
Deleting unattached EBS volumes containing manual backups.

### Guardrail
- Snapshot before deletion
- Require owner notification
- Add quarantine period before permanent deletion

---

## 4. Observability

### Metrics

| Metric | Source | Alert Threshold |
|---|---|---|
| orphan_resources_total | Janitor scan | > 20 |
| estimated_monthly_waste_usd | Report aggregation | > $500 |
| janitor_scan_duration_seconds | Workflow runtime | > 300 sec |
| deletion_failures_total | Delete operations | > 0 |
| untagged_resources_total | Tag scanner | > 10 |

### Publishing Targets

- CloudWatch (AWS)
- Prometheus
- Grafana dashboards
- Slack alerting via webhook

---

## 5. What Was Intentionally Left Out

This implementation intentionally avoids real AWS account execution, distributed scheduling, advanced FinOps analytics, RBAC dashboards, and automatic remediation approval systems. The focus was to build a safe, locally reproducible proof-of-concept that demonstrates Infrastructure as Code, orphan resource detection, CI/CD integration, tagging governance, and safe deletion workflows without incurring real cloud costs.
