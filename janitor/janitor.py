import boto3
import json
import argparse
import sys

from datetime import datetime, timezone
from constants import (
    EBS_GP3_COST_PER_GB,
    EIP_MONTHLY_COST,
    REQUIRED_TAGS
)

AWS_REGION = "us-east-1"

ec2 = boto3.client(
    "ec2",
    region_name=AWS_REGION,
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

findings = []


def get_tag_dict(tags):
    if not tags:
        return {}

    return {tag["Key"]: tag["Value"] for tag in tags}


def has_missing_tags(tags):
    return list(set(REQUIRED_TAGS) - set(tags.keys()))

def add_finding(
    resource_id,
    resource_type,
    reason,
    age_days,
    estimated_cost,
    tags,
    suggested_action,
    safe_to_auto_delete
):
    findings.append({
        "resource_id": resource_id,
        "resource_type": resource_type,
        "reason": reason,
        "age_days": age_days,
        "estimated_monthly_cost_usd": round(estimated_cost, 2),
        "tags": tags,
        "suggested_action": suggested_action,
        "safe_to_auto_delete": safe_to_auto_delete
    })


def scan_ebs(delete_mode):
    response = ec2.describe_volumes()

    for volume in response["Volumes"]:
        state = volume["State"]

        if state == "available":
            volume_id = volume["VolumeId"]
            size = volume["Size"]

            tags = get_tag_dict(volume.get("Tags", []))

            protected = tags.get("Protected", "false").lower() == "true"

            estimated_cost = size * EBS_GP3_COST_PER_GB

            create_time = volume["CreateTime"]
            age_days = (datetime.now(timezone.utc) - create_time).days

            add_finding(
                volume_id,
                "ebs_volume",
                "unattached",
                age_days,
                estimated_cost,
                tags,
                "delete",
                not protected
            )

            if delete_mode and not protected:
                ec2.delete_volume(VolumeId=volume_id)


def scan_stopped_instances(delete_mode, stopped_days):
    response = ec2.describe_instances()

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:

            state = instance["State"]["Name"]

            if state == "stopped":

                instance_id = instance["InstanceId"]

                tags = get_tag_dict(instance.get("Tags", []))

                protected = tags.get("Protected", "false").lower() == "true"

                launch_time = instance["LaunchTime"]

                age_days = (
                    datetime.now(timezone.utc) - launch_time
                ).days

                if age_days >= stopped_days:

                    add_finding(
                        instance_id,
                        "ec2_instance",
                        f"stopped_for_{stopped_days}_days",
                        age_days,
                        5.00,
                        tags,
                        "terminate",
                        not protected
                    )

                    if delete_mode and not protected:
                        ec2.terminate_instances(
                            InstanceIds=[instance_id]
                        )


def scan_eips(delete_mode):
    response = ec2.describe_addresses()

    for address in response["Addresses"]:

        instance_id = address.get("InstanceId")

        # orphaned if None OR empty
        if not instance_id:

            allocation_id = address.get("AllocationId")
            public_ip = address.get("PublicIp")

            resource_id = allocation_id if allocation_id else public_ip

            add_finding(
                resource_id,
                "elastic_ip",
                "unassociated",
                0,
                EIP_MONTHLY_COST,
                {},
                "release",
                True
            )

            if delete_mode and allocation_id:
                ec2.release_address(AllocationId=allocation_id)


def scan_missing_tags():
    response = ec2.describe_instances()

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:

            instance_id = instance["InstanceId"]
            tags = get_tag_dict(instance.get("Tags", []))

            missing = has_missing_tags(tags)

            if missing:
                add_finding(
                    instance_id,
                    "ec2_instance",
                    f"missing_tags:{','.join(missing)}",
                    0,
                    0,
                    tags,
                    "tag_resource",
                    False
                )


def generate_report():
    total_cost = sum(
        finding["estimated_monthly_cost_usd"]
        for finding in findings
    )

    report = {
        "scan_timestamp": datetime.now(
            timezone.utc
        ).strftime("%Y-%m-%dT%H:%M:%SZ"),

        "account_id": "000000000000",

        "region": AWS_REGION,

        "summary": {
            "total_orphans": len(findings),
            "estimated_monthly_waste_usd": round(total_cost, 2)
        },

        "findings": findings
    }

    with open("report.json", "w") as f:
        json.dump(report, f, indent=2)

    generate_markdown(report)


def generate_markdown(report):

    lines = []

    lines.append("# NimbusKart Cost Janitor Report")
    lines.append("")
    lines.append(
        f"Total Findings: {report['summary']['total_orphans']}"
    )

    lines.append(
        f"Estimated Monthly Waste: "
        f"${report['summary']['estimated_monthly_waste_usd']}"
    )

    lines.append("")

    for finding in report["findings"]:

        lines.append(
            f"- {finding['resource_type']} "
            f"({finding['resource_id']}): "
            f"{finding['reason']}"
        )

    with open("summary.md", "w") as f:
        f.write("\n".join(lines))


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete orphaned resources"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Dry run mode"
    )

    parser.add_argument(
        "--stopped-days",
        type=int,
        default=14
    )

    args = parser.parse_args()

    delete_mode = args.delete

    scan_ebs(delete_mode)
    scan_stopped_instances(
        delete_mode,
        args.stopped_days
    )
    scan_eips(delete_mode)
    scan_missing_tags()

    generate_report()

    if findings and not delete_mode:
        sys.exit(1)


if __name__ == "__main__":
    main()
