from core.llm_client import client as LLMClient
from repositories import vector_repo


def retrieve_relevant_chunks(question: str, case_id: int):

    embedding = (
        LLMClient.embeddings.create(
            model="gemini-embedding-001",
            input=question,
        )
        .data[0]
        .embedding
    )

    results = vector_repo.query_vectors(embedding=embedding, case_id=case_id)

    return results
