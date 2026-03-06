from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from core.database import get_session
from schemas.auth_schemas import TokenUserResponse, UserSignup
from services.auth_service import user_signin, user_signup

router = APIRouter()


@router.post(
    "/signup",
    response_model=TokenUserResponse,
    status_code=201,
    summary="user signs up",
)
def signup(body: UserSignup, session: Session = Depends(get_session)):
    return user_signup(session=session, body=body)


@router.post(
    "/signin",
    response_model=TokenUserResponse,
    status_code=200,
    summary="user signs in",
)
def signin(
    formdata: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    return user_signin(session=session, formdata=formdata)
