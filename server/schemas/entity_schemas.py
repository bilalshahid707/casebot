from pydantic import BaseModel
from typing import List


class EntityResponse(BaseModel):
    name: str
    type: str
    aliases: List[str]


class RelationshipResponse(BaseModel):
    source_entity: str
    target_entity: str
    relationship_type: str
    confidence: str


class ExtractionResponse(BaseModel):
    entities: List[EntityResponse]
    relationships: List[RelationshipResponse]
