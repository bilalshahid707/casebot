import boto3
from dotenv import load_dotenv
import os

load_dotenv()

s3 = boto3.client(
    service_name="s3",
    # Provide your R2 endpoint: https://<ACCOUNT_ID>.r2.cloudflarestorage.com
    endpoint_url=os.environ.get("S3_API"),
    # Provide your R2 Access Key ID and Secret Access Key
    aws_access_key_id=os.environ.get("R2_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("R2_Secret_Access_Key"),
    region_name="auto",  # Required by boto3, not used by R2
)
