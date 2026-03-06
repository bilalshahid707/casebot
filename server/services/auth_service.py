import os
from datetime import timedelta

from dotenv import load_dotenv
from fastapi import status

from helpers.security import create_access_token, get_password_hash, verify_password
from repositories import user_repo
from schemas.auth_schemas import TokenUserResponse
from schemas.user_schemas import ReadUser
from core.exceptions import AppException
from fastapi import status

load_dotenv()


def user_signin(session, formdata):
    user = user_repo.get_user_by_username(session, formdata.username)
    if not user or not verify_password(formdata.password, user.password):
        raise AppException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Incorrect username or password",
        )
    access_token_expires = timedelta(
        minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return TokenUserResponse(
        access_token=access_token,
        token_type="bearer",
        user=ReadUser(id=user.id, username=user.username),
        access_token_expires=access_token_expires,
    )


def user_signup(session, body):
    hashed_password = get_password_hash(body.password)
    user = user_repo.create_user(
        session=session, username=body.username, hashed_password=hashed_password
    )
    access_token_expires = timedelta(
        minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return TokenUserResponse(
        access_token=access_token,
        token_type="bearer",
        user=ReadUser(id=user.id, username=user.username),
        access_token_expires=access_token_expires,
    )
