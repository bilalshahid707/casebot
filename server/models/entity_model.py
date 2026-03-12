from sqlmodel import SQLModel, Field, create_engine, Session, select, Relationship
from typing import Optional
from datetime import datetime


# ── Models ─────────────────────────────────────────────────────────────────────


class Entity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str
    aliases: Optional[str] = None
    case_id: int = Field(foreign_key="case.id")
    asset_id: int = Field(foreign_key="asset.id")


class EntityRelationship(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source_entity_id: int = Field(foreign_key="entity.id")
    target_entity_id: int = Field(foreign_key="entity.id")
    case_id: int = Field(foreign_key="case.id")
    asset_id: int = Field(foreign_key="asset.id")
    relationship_type: str
    confidence: str = "HIGH"
