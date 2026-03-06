from enum import Enum
from typing import List
from sqlmodel import SQLModel, Field, Relationship


class CaseStatus(str, Enum):
    active = "active"
    archive = "archive"


class Case(SQLModel, table=True):
    id: int = Field(primary_key=True)
    case_number: int = Field(nullable=False)
    case_name: str = Field(nullable=False)
    opposing_party: str = Field(nullable=True)
    client: str = Field(nullable=True)
    status: CaseStatus = Field(default=CaseStatus.active)
    user_id: int = Field(nullable=False, foreign_key="user.id")
    processed: bool = Field(default=False)
    assets: List["Asset"] = Relationship(back_populates="case")
