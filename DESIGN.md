# DESIGN.md

## Multi-Cloud Design

The current Janitor is AWS-focused using boto3, but the core can be extended for GCP and Azure by separating provider-specific logic from the scanning engine.

### Proposed Structure

```
janitor/
├── core/          # reporting, policies, scan engine
├── providers/
│   ├── aws/
│   ├── gcp/
│   └── azure/
└── shared/
 id="9zwtgu"
```
Each provider would return resources in a common schema so the core logic does not need to change when adding new clouds.

---

## IAM Permissions

### Dry-Run Mode
Read-only access:
- ec2:DescribeInstances
- ec2:DescribeVolumes
- ec2:DescribeAddresses
- ec2:DescribeSnapshots
- s3:ListAllMyBuckets

### Delete Mode
Additional permissions:
- ec2:DeleteVolume
- ec2:TerminateInstances
- ec2:ReleaseAddress

### Minimal Read-Only Policy

```json id="dh1we0"
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
        "s3:ListAllMyBuckets"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## Safety Nets

### Failure Mode 1
A stopped EC2 instance used for disaster recovery could be deleted accidentally.

Guardrails:
- Skip resources tagged `Protected=true`
- Add minimum age threshold before deletion
- Introduce approval workflow in production

### Failure Mode 2
An unattached EBS volume containing backup data could be removed.

Guardrails:
- Snapshot before deletion
- Add retention/quarantine period
- Skip resources tagged `Backup=true`

---

## Observability

| Metric | Source | Alert Threshold |
|---|---|---|
| orphan_resources_total | Janitor scan | > 20 |
| estimated_monthly_waste_usd | report.json | > $500 |
| janitor_scan_duration_seconds | GitHub Actions runtime | > 300 sec |
| deletion_failures_total | Janitor logs | > 0 |
| untagged_resources_total | Tag scan | > 10 |

Metrics can be published to CloudWatch, Prometheus, or Grafana dashboards.

---

## What Was Not Built

This project focuses on a safe local proof-of-concept using Terraform, LocalStack, Python, and GitHub Actions. Multi-account support, real AWS billing integration, approval-based deletion workflows, dashboards, and scheduled production deployments were intentionally left out to keep the implementation simple, reproducible, and cost-free for evaluation purposes.
```
