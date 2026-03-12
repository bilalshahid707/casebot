from fastapi import Depends, HTTPException, status
from sqlmodel import Session
import logging as logger
from core.database import get_session
from core.s3 import s3
from core.exceptions import (
    ForbiddenException,
    AppException,
)
from .auth_dependencies import get_current_user
from repositories import case_repo
from helpers.file_uploader import get_file_from_s3


def get_owned_case(
    case_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    case = case_repo.get_case_by_id(session=session, case_id=case_id)

    if case.user_id != current_user.id:
        raise ForbiddenException()

    return case


def get_asset_with_verification(
    asset_id: int,
    case_id: int,
    session: Session = Depends(get_session),
    case=Depends(get_owned_case),
):
    asset = case_repo.get_asset_by_id(session=session, asset_id=asset_id)

    if asset.case_id != case.id:
        raise ForbiddenException()

    file = get_file_from_s3(key=asset.asset_name)
    return file
