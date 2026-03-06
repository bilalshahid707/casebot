from pydantic import BaseModel

from schemas.user_schemas import ReadUser
from datetime import timedelta


class TokenUserResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: ReadUser
    access_token_expires: timedelta


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserSignup(BaseModel):
    username: str
    password: str
