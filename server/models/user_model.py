from enum import Enum
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class RoleEnum(str, Enum):
    ADMIN = "admin"
    ATTORNEY = "attorney"
    PARALEGAL = "paralegal"


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(default=None, nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_by: int = Field(nullable=True, foreign_key="user.id")
    role: RoleEnum = Field(default=RoleEnum.ATTORNEY)
    created_at: datetime = Field(default_factory=datetime.now)
