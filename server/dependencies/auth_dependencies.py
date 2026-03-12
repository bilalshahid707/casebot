import os
from typing import Annotated, List

import jwt
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from core.exceptions import ForbiddenException, UnauthorizedException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from schemas.auth_schemas import TokenData
from repositories import user_repo
from core.database import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin")

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        username = payload.get("sub")
        if username is None:
            raise UnauthorizedException(message="Could not validate credentials")
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise UnauthorizedException(message="Could not validate credentials")
    user = user_repo.get_user_by_username(session=session, username=token_data.username)
    return user


def restrict_to(roles: List):
    def role_checker(
        current_user: Annotated[user_repo.User, Depends(get_current_user)],
    ):
        if current_user.role not in roles:
            raise ForbiddenException()
        return current_user

    return role_checker
