from enum import Enum
from typing import Optional

from pydantic import BaseModel


class RoleEnum(str, Enum):
    ATTORNEY = "ATTORNEY"
    ADMIN = "ADMIN"
    STAFF = "STAFF"


class CreateUser(BaseModel):
    username: str
    role: RoleEnum = RoleEnum.ATTORNEY
    password: str
    created_by: Optional[int] = None


class ReadUser(BaseModel):
    id: int
    username: str
