from core.llm_client import client as LLMClient
import json
from .instructions import SYSTEM_INSTRUCTIONS
from schemas.entity_schemas import ExtractionResponse


class EntityExtractionAgent:

    def __init__(self):
        self.client = LLMClient
        self.model = "gemini-2.5-flash"

    def extract(self, parsed_documents) -> ExtractionResponse:
        docs_to_string = [[doc.model_dump() for doc in parsed_documents]]
        content = json.dumps(docs_to_string, indent=2)

        response = self.client.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                {"role": "user", "content": content},
            ],
            response_format=ExtractionResponse,
        )

        return response.choices[0].message.parsed
