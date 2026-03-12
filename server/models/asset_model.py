from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


class AssetStatus(Enum):
    uploading = "uploading"
    processed = "processed"


class Asset(SQLModel, table=True):
    id: int = Field(primary_key=True)
    case_id: int = Field(nullable=False, foreign_key="case.id")
    asset_URL: str = Field(nullable=False)
    asset_name: str = Field(nullable=False)
    case: "Case" = Relationship(back_populates="assets")
    status: AssetStatus = Field(default=AssetStatus.uploading)
    is_extracted: bool = Field(default=False)
