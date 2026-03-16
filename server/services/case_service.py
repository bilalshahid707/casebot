from pydoc import doc

from fastapi import status, BackgroundTasks
from sqlmodel import Session
from dotenv import load_dotenv
import os
from schemas.case_schemas import CaseCreate, CaseUpdate, AssetUpdate
from repositories import case_repo
from core.s3 import s3
from services import embedding_service as EmbeddingService
from helpers.constants import allowed_file_formats
from core.exceptions import AppException, ForbiddenException
from helpers.file_uploader import upload_file_to_s3

load_dotenv()


def create_case(case_data: CaseCreate, session: Session, current_user):

    if current_user.role != "attorney":
        raise ForbiddenException(message="only attorneys can create case")

    return case_repo.create_case(session, case_data, current_user.id)


def get_case_by_Id(case_id: int, session: Session):
    return case_repo.get_case_by_id(session, case_id)


def get_cases_by_user_id(user_id: int, session: Session):
    return case_repo.get_cases_by_user_id(session, user_id)


def update_case(case_id: int, case_data: CaseUpdate, session: Session):
    return case_repo.update_case(session, case_id, case_data)


async def upload_case_asset(
    case_id: int,
    file,
    session: Session,
):
    if file.content_type not in allowed_file_formats:
        raise AppException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Unsupported file type. Only PDF, TXT, JPEG, and PNG files are allowed.",
        )

    file_content = await file.read()

    upload_file_to_s3(file.filename, file_content, file.content_type)

    asset_data = {
        "file_name": file.filename,
        "file_url": f"{os.environ.get('R2_PUBLIC_URL')}/{file.filename}",
    }
    asset = case_repo.create_asset(session, asset_data, case_id)

    return asset


def get_case_assets(case_id: int, session: Session):
    return case_repo.get_case_assets(session=session, case_id=case_id)


def update_asset(asset_id: int, session: Session, asset_data: AssetUpdate):
    return case_repo.update_asset(
        session=session, asset_data=asset_data, asset_id=asset_id
    )


def process_case_asset(
    case_id: int,
    asset_id: int,
    file,
    session: Session,
    background_tasks: BackgroundTasks,
):
    try:
        EmbeddingService.process_and_store_embeddings(
            file, case_id, asset_id, session, background_tasks
        )
    except Exception as e:
        raise AppException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"Failed to process file: {str(e)}",
        )
