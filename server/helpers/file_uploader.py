from core.s3 import s3
from core.exceptions import AppException, NotFoundException


def upload_file_to_s3(key: str, content: bytes, content_type: str):
    try:
        s3.put_object(
            Bucket="casebot",
            Key=key,
            Body=content,
            ContentType=content_type,
        )
    except Exception as e:
        raise AppException(message="Failed to upload file")


def get_file_from_s3(key: str):

    try:
        response = s3.get_object(Bucket="casebot", Key=key)
        file_content = response["Body"].read()
        content_type = response["ContentType"]
        return {"filename": key, "content_type": content_type, "content": file_content}
    except s3.exceptions.NoSuchKey:
        raise NotFoundException()
    except Exception as e:
        raise AppException(message="Failed to fetch file")
