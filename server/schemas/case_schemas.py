from pydantic import BaseModel
from typing import Optional, List
from models.case_model import CaseStatus


class AssetRead(BaseModel):
    id: int
    asset_URL: str
    asset_name: str


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
    assets: List[AssetRead]


class CaseUpdate(BaseModel):
    case_number: Optional[int] = None
    case_name: Optional[str] = None
    opposing_party: Optional[str] = None
    client: Optional[str] = None
    status: Optional[CaseStatus] = None
    processed: Optional[bool] = None


class EntityRead(BaseModel):
    id: Optional[int]
    name: str
    type: str
    aliases: Optional[str]
    case_id: int


class RelationshipRead(BaseModel):
    id: Optional[int]
    source_entity: EntityRead
    target_entity: EntityRead
    relationship_type: str


class AssetUpdate(BaseModel):
    status: Optional[CaseStatus]
    is_extracted: Optional[bool]
