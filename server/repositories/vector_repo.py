from core.pinecone import pc
import uuid
from core.exceptions import AppException

index = pc.Index("casebot-index")


def upsert_vectors(chunks, case_id: int, asset_id: int, response):
    vectors = []

    for chunk, emb in zip(chunks, response.data):

        vectors.append(
            {
                "id": str(uuid.uuid4()),
                "values": emb.embedding,
                "metadata": {
                    # Typecasting both case_id and asset_id to int to ensure they are stored as integers in Pinecone for querying and filtering
                    "case_id": int(case_id),
                    "asset_id": int(asset_id),
                    "source": chunk.metadata.get("source", ""),
                    "page": chunk.metadata.get("page_number", 0),
                    "text": chunk.page_content,
                },
            }
        )

    try:
        index.upsert(vectors=vectors)
    except Exception as e:
        raise AppException(
            message=f"Failed to upsert vectors: {str(e)}", status_code=500
        )


def query_vectors(embedding: list, case_id: int):

    try:
        results = index.query(
            vector=embedding,
            top_k=25,
            include_metadata=True,
            filter={"case_id": int(case_id)},
        )
    except Exception as e:
        raise AppException(
            message=f"Failed to query vectors: {str(e)}", status_code=500
        )
    chunks = [
        {
            "text": result["metadata"]["text"],
            "source": result["metadata"]["source"],
            "page": result["metadata"]["page"],
        }
        for result in results["matches"]
    ]

    return chunks
