from sqlmodel import Session
from core.llm_client import client as LLMClient
from helpers.text_splitter import text_splitter
from repositories import vector_repo
from .insight_service import get_entity_relationship
from services import case_service
from fastapi import BackgroundTasks


def process_and_store_embeddings(
    file,
    case_id: int,
    asset_id: int,
    session: Session,
    background_tasks: BackgroundTasks,
):

    # File object is coming from case dependency that will be used by text splitter
    chunks = text_splitter(file)

    response = LLMClient.embeddings.create(
        model="gemini-embedding-001",
        input=[chunk.page_content for chunk in chunks],
    )

    vector_repo.upsert_vectors(
        chunks=chunks,
        case_id=case_id,
        asset_id=asset_id,
        response=response,
    )

    case_service.update_asset(
        asset_data={"status": "processed"}, asset_id=asset_id, session=session
    )
    background_tasks.add_task(get_entity_relationship, case_id, session)

    return {"status": "success"}
