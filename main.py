from compliance_checker import find_non_compliant_buckets
from remediation import remediate_s3_bucket

def main():
    """Main function to check compliance and remediate non-compliant resources."""
    print("Checking for non-compliant S3 buckets...")
    non_compliant_buckets = find_non_compliant_buckets()

    if not non_compliant_buckets:
        print("All S3 buckets are compliant!")
        return

    print(f"Found {len(non_compliant_buckets)} non-compliant buckets: {non_compliant_buckets}")

    for bucket in non_compliant_buckets:
        print(f"Remediating bucket: {bucket}")
        remediate_s3_bucket(bucket)

if __name__ == "__main__":
    main()
