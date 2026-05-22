# Approximate AWS pricing references:
# EBS gp3: https://aws.amazon.com/ebs/pricing/
# Elastic IP: https://aws.amazon.com/ec2/pricing/on-demand/

EBS_GP3_COST_PER_GB = 0.08
EIP_MONTHLY_COST = 3.60

REQUIRED_TAGS = [
    "Project",
    "Environment",
    "Owner"
]
