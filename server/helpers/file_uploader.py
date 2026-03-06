from core.s3 import s3
from core.exceptions import AppException
from fastapi import status


def upload_file_to_s3(key: str, content: bytes, content_type: str):
    try:
        s3.put_object(
            Bucket="casebot",
            Key=key,
            Body=content,
            ContentType=content_type,
        )
    except Exception as e:
        raise AppException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="File upload failed",
        )
