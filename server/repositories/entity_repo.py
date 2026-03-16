from sqlmodel import Session, select
from typing import Optional
from models.entity_model import Entity, EntityRelationship
from sqlalchemy.orm import aliased
from core.exceptions import NotFoundException


def get_entity_by_name(session: Session, name: str) -> Optional[Entity]:
    return session.exec(select(Entity).where(Entity.name == name)).first()


def get_existing_entity(
    session: Session, name: str, asset_id: int, case_id: int
) -> Optional[Entity]:
    return session.exec(
        select(Entity).where(
            Entity.name == name, Entity.asset_id == asset_id, Entity.case_id == case_id
        )
    ).first()


def create_entity(
    session: Session,
    case_id: int,
    name: str,
    type: str,
    asset_id,
    aliases: Optional[str] = None,
) -> Optional[Entity]:
    existing = get_existing_entity(session, name, asset_id=asset_id, case_id=case_id)
    if existing:
        return
    entity = Entity(
        name=name, type=type, aliases=aliases, case_id=case_id, asset_id=asset_id
    )
    session.add(entity)
    session.commit()
    session.refresh(entity)
    return entity


def create_relationship(
    session: Session,
    case_id: int,
    asset_id: int,
    source_name: str,
    target_name: str,
    relationship_type: str,
    confidence: str = "HIGH",
) -> Optional[EntityRelationship]:
    source = get_existing_entity(
        session, source_name, asset_id=asset_id, case_id=case_id
    )
    if not source:
        return

    target = get_existing_entity(
        session, target_name, asset_id=asset_id, case_id=case_id
    )
    if not target:
        return

    rel = EntityRelationship(
        source_entity_id=source.id,
        target_entity_id=target.id,
        relationship_type=relationship_type,
        confidence=confidence,
        case_id=case_id,
        asset_id=asset_id,
    )
    session.add(rel)
    session.commit()
    session.refresh(rel)
    return rel


def get_relationships_by_case_id(session: Session, case_id: int) -> list[dict]:
    source = aliased(Entity)
    target = aliased(Entity)

    results = session.exec(
        select(EntityRelationship, source, target)
        .join(source, EntityRelationship.source_entity_id == source.id)
        .join(target, EntityRelationship.target_entity_id == target.id)
        .where(EntityRelationship.case_id == case_id)
    ).all()
    if not results:
        raise NotFoundException(message="No entities found")
    return [
        {
            "id": rel.id,
            "relationship_type": rel.relationship_type,
            "confidence": rel.confidence,
            "source_entity": source_entity,
            "target_entity": target_entity,
        }
        for rel, source_entity, target_entity in results
    ]


def get_entities_by_case_id(session: Session, case_id: int) -> list[Entity]:
    results = session.exec(select(Entity).where(Entity.case_id == case_id)).all()

    if not results:
        raise NotFoundException(message="No entities found")
    return results
