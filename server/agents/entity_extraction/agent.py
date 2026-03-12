from core.llm_client import client as LLMClient
import json
from .instructions import SYSTEM_INSTRUCTIONS
from schemas.entity_schemas import ExtractionResponse


class EntityExtractionAgent:

    def extract(self, parsed_documents) -> ExtractionResponse:
        docs_to_string = []
        for doc in parsed_documents:
            docs_to_string.append(doc.model_dump())
        content = json.dumps(docs_to_string, indent=2)
        response = LLMClient.chat.completions.parse(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                {"role": "user", "content": content},
            ],
            response_format=ExtractionResponse,
        )

        return response.choices[0].message.parsed
