from sqlmodel import SQLModel, Field
from enum import Enum
from typing import List
from sqlalchemy import JSON
from sqlalchemy import Column


class MessageRole(str, Enum):
    User = "user"
    Assistant = "assistant"
    System = "system"


class Message(SQLModel, table=True):
    id: int = Field(primary_key=True)
    case_id: int = Field(nullable=False, foreign_key="case.id")
    role: str = Field(nullable=False)
    content: str = Field(nullable=False)
    citations: List[dict] = Field(default=[], sa_column=Column(JSON, nullable=False))
