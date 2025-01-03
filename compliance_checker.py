import boto3
from botocore.exceptions import ClientError

session = boto3.Session(
    aws_access_key_id= "your-access-key",
    aws_secret_access_key= "your-secret-key",
    region_name= "specify-region"
)
# AWS Clients
s3_client = session.client('s3')

def find_non_compliant_buckets():
    """Identify S3 buckets that do not have server-side encryption enabled."""
    buckets = s3_client.list_buckets()["Buckets"]
    print(buckets)
    non_compliant_buckets = []
    for bucket in buckets:
        bucket_name = bucket["Name"]
        try:
            encryption = s3_client.get_bucket_encryption(Bucket=bucket_name)
            print(encryption)
            rules = encryption.get("ServerSideEncryptionConfiguration", {}).get("Rules", [])
            if not rules:
                raise Exception("No encryption rules found")
        except Exception:
            non_compliant_buckets.append(bucket_name)
            continue

        try:
            # Get the encryption configuration for the bucket
            response = s3_client.get_bucket_encryption(Bucket=bucket_name)
            
            # Check if the encryption is applied with KMS
            encryption = response.get('ServerSideEncryptionConfiguration', {}).get('Rules', [])
            if encryption:
                for rule in encryption:
                    # Check if the encryption is applied using KMS
                    if rule.get('ApplyServerSideEncryptionByDefault', {}).get('SSEAlgorithm') == 'aws:kms':
                        kms_key_id = rule.get('ApplyServerSideEncryptionByDefault', {}).get('KMSMasterKeyID', 'Not Provided')
                        print(f"KMS encryption is applied with key ID: {kms_key_id}")
                    else:
                        print("Encryption is applied, but not using KMS.")
                        non_compliant_buckets.append(bucket_name)
            else:
                print("No encryption applied.")

        except ClientError as e:
            # If the bucket doesn't exist or the encryption configuration is not found
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                print("No encryption configuration found.")
            else:
                print(f"Error occurred: {e}")
    print(non_compliant_buckets)
    return non_compliant_buckets
