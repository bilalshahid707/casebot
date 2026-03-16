import boto3
from dotenv import load_dotenv
import os

load_dotenv()

s3 = boto3.client(
    service_name="s3",
    endpoint_url=os.environ.get("S3_API"),
    aws_access_key_id=os.environ.get("R2_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("R2_Secret_Access_Key"),
    region_name="auto",
)
