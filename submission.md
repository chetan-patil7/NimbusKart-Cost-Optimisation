# Submission — DevOps Engineer Assignment

**Candidate name:** Chetan Patil
**Email:**
**Date submitted:** 2026-05-25
**Hours spent (approximate):** ~20–25 hours

## Deliverables checklist

* [x] Part A: Terraform code under /terraform applies cleanly on LocalStack
* [x] Part A: `terraform validate` and `terraform fmt -check` both pass
* [x] Part B: Janitor script runs in --dry-run mode and produces report.json
* [x] Part B: GitHub Actions workflow runs green on a fresh PR
* [x] Part B: --delete mode respects Protected=true tag
* [x] Part C: DESIGN.md is present and within 2 pages
* [x] Walkthrough video link below is accessible (unlisted is fine)

## Walkthrough video

Link (Loom / YouTube unlisted / Google Drive):https://www.loom.com/share/49af935ea85d4ed6ad96742c93080619

Length: max 5 minutes

## Sample report

Path to a sample report.json produced by your script:

`(https://github.com/chetan-patil7/NimbusKart-Cost-Optimisation/blob/main/samples/report.json)`

## Known limitations

* Uses LocalStack instead of real AWS, so behavior may differ from production AWS APIs
* No persistent database for historical cost tracking (reports are file-based only)
* No dashboard or visualization layer for cost trends
* Limited rule engine (static REQUIRED_TAGS list instead of policy-as-code tools)

## AI usage disclosure

Used Chatgpt's assistance for debugging Terraform + LocalStack issues, improving Python scanning logic, structuring GitHub Actions workflow, and refining documentation. All final implementation decisions and validation were done manually.
