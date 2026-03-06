from dotenv import load_dotenv
import os
from openai import OpenAI
from .instructions import system_instructions
from services import chunk_service as ChunkService
from pydantic import BaseModel

load_dotenv()


class ResponseModel(BaseModel):
    response: str
    citations: list[dict]


class ChatAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        self.model = "gemini-2.5-flash"

    def reply(self, message: str, case_id: int):

        chunks = ChunkService.retrieve_relevant_chunks(message, case_id)

        if not chunks:
            return "No relevant case documents found."

        response = self.client.chat.completions.parse(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_instructions,
                },
                {
                    "role": "system",
                    "content": f"Case Document Context:\n{chunks}",
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            response_format=ResponseModel,
        )

        return response.choices[0].message.parsed
