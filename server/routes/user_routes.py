import os
from typing import Annotated

from fastapi import APIRouter, Depends

from models.user_model import User
from schemas.user_schemas import ReadUser
from dependencies import auth_dependencies as AuthDependencies

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

router = APIRouter()


@router.get("/me", response_model=ReadUser, status_code=200, summary="get current user")
def get_me(
    current_user: Annotated[User, Depends(AuthDependencies.get_current_user)],
):
    return ReadUser(id=current_user.id, username=current_user.username)
