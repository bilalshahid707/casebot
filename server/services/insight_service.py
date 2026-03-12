from sqlmodel import Session, select
from models.asset_model import Asset, AssetStatus
from agents.entity_extraction.agent import EntityExtractionAgent
from helpers.file_uploader import get_file_from_s3
from helpers.document_parser import parse_file_to_documents
from repositories import entity_repo
from collections import defaultdict
from core.exceptions import AppException
from fastapi import status
from services import case_service


def get_entity_relationship(case_id: int, session: Session) -> dict:

    assets = session.exec(
        select(Asset).where(
            Asset.case_id == case_id,
            Asset.status == AssetStatus.processed,
            Asset.is_extracted == False,
        )
    ).all()

    if not assets:
        return {"status": "nothing_to_process", "chunks_processed": 0}

    agent = EntityExtractionAgent()

    for asset in assets:
        file = get_file_from_s3(asset.asset_name)
        parsed_documents = parse_file_to_documents(file)
        try:
            extracted = agent.extract(parsed_documents=parsed_documents)

            for entity in extracted.entities:
                entity = entity_repo.create_entity(
                    session=session,
                    name=entity.name,
                    type=entity.type,
                    aliases=entity.aliases,
                    case_id=case_id,
                    asset_id=asset.id,
                )
            for rel in extracted.relationships:
                rel = entity_repo.create_relationship(
                    session=session,
                    source_name=rel.source_entity,
                    target_name=rel.target_entity,
                    relationship_type=rel.relationship_type,
                    confidence=rel.confidence,
                    case_id=case_id,
                    asset_id=asset.id,
                )

            case_service.update_asset(
                asset_data={"is_extracted": True}, asset_id=asset.id, session=session
            )
        except Exception as e:
            print(f"{e}")
            continue

    return {"status": "success", "files_processed": "processed"}


def get_case_relationships(case_id: int, session: Session) -> dict:
    relationships = entity_repo.get_relationships_by_case_id(
        session=session, case_id=case_id
    )

    if not relationships:
        raise AppException(
            message="No relationships have been created for the case",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # graph = defaultdict(list)

    # for rel in relationships:
    #     src = rel["source_entity"].name
    #     tgt = rel["target_entity"].name
    #     rel = rel["relationship_type"]

    #     graph[src].append({"entity": tgt, "relationship": rel})

    return relationships


def get_case_entities(case_id: int, session: Session) -> dict:
    entities = entity_repo.get_entities_by_case_id(session=session, case_id=case_id)

    if not entities:
        raise AppException(
            message="No entities have been created for the case",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # graph = defaultdict(list)

    # for rel in relationships:
    #     src = rel["source_entity"].name
    #     tgt = rel["target_entity"].name
    #     rel = rel["relationship_type"]

    #     graph[src].append({"entity": tgt, "relationship": rel})

    return entities
