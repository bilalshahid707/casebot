from pydantic import BaseModel
from typing import Optional
from models.case_model import CaseStatus


class CaseCreate(BaseModel):
    case_number: int
    case_name: str
    opposing_party: Optional[str] = None
    client: Optional[str] = None


class CaseRead(BaseModel):
    id: int
    case_number: int
    case_name: str
    opposing_party: Optional[str]
    client: Optional[str]
    status: CaseStatus
    user_id: int


class CaseUpdate(BaseModel):
    case_number: Optional[int] = None
    case_name: Optional[str] = None
    opposing_party: Optional[str] = None
    client: Optional[str] = None
    status: Optional[CaseStatus] = None
    processed: Optional[bool] = None
