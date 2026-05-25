# 1. Multi-Cloud Reality

Explain:

### Problem

Currently Janitor works only for AWS.

NimbusKart wants:

* GCP later
* Azure later

So explain:

* how you would avoid rewriting everything.

### Include

* modular architecture
* provider abstraction
* separate provider adapters

### Mention

Example structure:

```text id="l2sk7u"
core/
providers/aws/
providers/gcp/
providers/azure/
```

### Explain

* core logic remains same
* only provider-specific SDK code changes

---

# 2. Permissions

Explain:
What permissions are needed in:

## Dry-run mode

Only read permissions.

Examples:

* DescribeInstances
* DescribeVolumes
* DescribeAddresses

## Delete mode

Needs destructive permissions.

Examples:

* DeleteVolume
* TerminateInstances
* ReleaseAddress

### IMPORTANT

Include:

* minimal IAM JSON policy

This is mandatory.

---

# 3. Safety Net

Need:

## Two real outage scenarios

Examples:

### Scenario 1

Deleting stopped EC2 used for DR/backups.

### Scenario 2

Deleting unattached EBS containing important data.

---

## Then explain guardrails

Examples:

* `Protected=true`
* approval workflow
* quarantine period
* snapshot before delete
* age thresholds

This section is very important for scoring.

---

# 4. Observability

Need:

* metrics
* source
* threshold

Usually in table format.

Examples:

| Metric                      | Source       | Alert |
| --------------------------- | ------------ | ----- |
| orphan_resources_total      | janitor scan | >20   |
| estimated_monthly_waste_usd | report.json  | >500  |

Need around:

* 3 to 5 metrics

Also mention:

* CloudWatch
* Prometheus
* Grafana
* Slack alerts

---

# 5. What You Did NOT Build

This is about:

* honest scoping

Mention things intentionally skipped.

Examples:

* multi-account support
* real billing APIs
* RBAC dashboards
* approval systems

Then explain:

* kept project lightweight
* focused on safe local reproducible demo

---
