import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# 1. ENTER YOUR DATA
ACCESS_KEY = 'AKIA2LOVOPGLHKMLZHM7'
SECRET_KEY = 'sKtBYG76ljGRkBRUyOT36rD+8F8Kp1diibtLmmrs'
BUCKET_NAME = 'sentinel-strategy-vault-01'

def verify_aws():
    print("🔍 Testing AWS Connection...")
    try:
        # Initialize the S3 client
        s3 = boto3.client(
            's3',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY
        )
        
        # Test 1: List Buckets (Verifies Credentials)
        response = s3.list_buckets()
        print("✅ Success! Connected to AWS.")
        print("Your available buckets:")
        for bucket in response['Buckets']:
            print(f"  - {bucket['Name']}")

        # Test 2: Permission Check (Verifies you can 'see' your specific bucket)
        s3.head_bucket(Bucket=BUCKET_NAME)
        print(f"✅ Success! Bucket '{BUCKET_NAME}' is accessible.")

    except NoCredentialsError:
        print("❌ Error: AWS credentials not found.")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '403':
            print("❌ Error: Access Denied (Check your IAM permissions).")
        elif error_code == '404':
            print(f"❌ Error: Bucket '{BUCKET_NAME}' does not exist.")
        else:
            print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    verify_aws()