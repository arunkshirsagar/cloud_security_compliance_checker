import subprocess
import logging

logging.basicConfig(filename='remediation.log', level=logging.INFO)

def remediate_s3_bucket(bucket_name):
    """Remediate non-compliant S3 bucket by enabling encryption."""
    try:
        print(f"Starting remediation for bucket: {bucket_name}")

        with open("terraform/terraform.tfvars", "w") as f:
            f.write(f'''bucket_name = "{bucket_name}"''')

        # Initialize Terraform
        subprocess.run(["terraform", "-chdir=terraform", "init"], check=True)

        # Import the existing bucket into Terraform state
        subprocess.run(
            ["terraform", "-chdir=terraform", "import", "aws_s3_bucket.remediate", bucket_name],
            check=True,
        )

        # Apply Terraform configuration to enable encryption
        subprocess.run(["terraform", "-chdir=terraform", "apply", "-auto-approve"], check=True)

        logging.info(f"Remediated bucket: {bucket_name}")
        print(f"Bucket {bucket_name} remediated successfully.")

        subprocess.run(["terraform", "-chdir=terraform", "state", "rm", "aws_s3_bucket.remediate"], check=True)

    except Exception as e:
        logging.error(f"Failed to remediate bucket {bucket_name}: {e}")
        print(f"Failed to remediate bucket {bucket_name}: {e}")
