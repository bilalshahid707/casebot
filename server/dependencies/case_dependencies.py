from fastapi import Depends, HTTPException, status
from sqlmodel import Session
import io

from core.database import get_session
from core.s3 import s3
from .auth_dependencies import get_current_user
from repositories import case_repo as CaseRepo


class S3FileObject:
    """Wrapper to make S3 content compatible with UploadFile interface"""

    def __init__(self, content: bytes, filename: str, content_type: str):
        self.file = io.BytesIO(content)
        self.filename = filename
        self.content_type = content_type

    async def read(self):
        return self.file.read()

    async def seek(self, offset):
        return self.file.seek(offset)

    def close(self):
        return self.file.close()


def get_owned_case(
    case_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    case = CaseRepo.get_case_by_id(session=session, case_id=case_id)

    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    if case.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this case",
        )

    return case


def get_asset_with_verification(
    asset_id: int,
    case_id: int,
    session: Session = Depends(get_session),
    case=Depends(get_owned_case),
):
    """
    Verify asset ownership and fetch asset data from S3.

    This dependency:
    1. Verifies the case ownership (via get_owned_case)
    2. Fetches the asset from the database
    3. Verifies the asset belongs to the specified case
    4. Fetches and returns the asset content from S3
    """
    asset = CaseRepo.get_asset_by_id(session=session, asset_id=asset_id)

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    if asset.case_id != case.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This asset does not belong to the specified case",
        )

    try:
        s3_response = s3.get_object(
            Bucket="casebot",
            Key=asset.asset_name,
        )
        asset_content = s3_response["Body"].read()
        content_type = s3_response["ContentType"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch asset from S3: {str(e)}",
        )

    # Return file object compatible with text_splitter
    file_object = {
        "content": asset_content,
        "filename": asset.asset_name,
        "content_type": content_type,
    }
    return file_object
