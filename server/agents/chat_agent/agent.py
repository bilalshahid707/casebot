from dotenv import load_dotenv
import os
from openai import OpenAI
from .instructions import system_instructions
from services import chunk_service as ChunkService
from schemas.chat_schemas import ChatResponse
from core.llm_client import client as LLMClient

load_dotenv()


class ChatAgent:
    def __init__(self):
        self.client = LLMClient
        self.model = "gemini-2.5-flash"

    def reply(self, message: str, case_id: int):

        chunks = ChunkService.retrieve_relevant_chunks(message, case_id)

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
            response_format=ChatResponse,
        )
        print(response.choices[0].message.parsed)
        return response.choices[0].message.parsed
