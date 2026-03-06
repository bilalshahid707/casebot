from sqlmodel import SQLModel, Field
from typing import Optional


class CaseSummary(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    case_id: int = Field(foreign_key="case.id", unique=True)
    content: str = Field(nullable=False)
    url: str = Field(nullable=False)
