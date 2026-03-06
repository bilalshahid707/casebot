import os
from typing import Annotated, List

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from core.exceptions import AppException
from fastapi.security import OAuth2PasswordBearer
from schemas.auth_schemas import TokenData
from repositories import user_repo as UserRepo
from core.database import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            os.environ.get("SECRET_KEY"),
            algorithms=[os.environ.get("ALGORITHM")],
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = UserRepo.get_user_by_username(session=session, username=token_data.username)
    if user is None:
        raise AppException(
            message="User not found", status_code=status.HTTP_404_NOT_FOUND
        )
    return user


def restrict_to(roles: List):
    def role_checker(
        current_user: Annotated[UserRepo.User, Depends(get_current_user)],
    ):
        if current_user.role not in roles:
            raise AppException(
                message="You do not have permission to perform this action",
                status_code=status.HTTP_403_FORBIDDEN,
            )
        return current_user

    return role_checker
