from sqlmodel import Session

from core.llm_client import client as LLMClient
from helpers.text_splitter import text_splitter
from repositories import vector_repo
from services import case_service


async def process_and_store_embeddings(
    file, case_id: int, asset_id: int, session: Session
):
    chunks = await text_splitter(file)

    response = LLMClient.embeddings.create(
        model="gemini-embedding-001",
        input=[chunk.page_content for chunk in chunks],
    )

    vector_repo.upsert_vectors(
        chunks=chunks, case_id=case_id, asset_id=asset_id, file=file, response=response
    )

    return {"status": "success"}
