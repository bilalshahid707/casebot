from typing import Optional
from dotenv import load_dotenv
import os
from openai import OpenAI
from base64 import b64encode
from .instructions import OCR_SYSTEM_INSTRUCTION
from core.llm_client import client as LLMClient

load_dotenv()


class OCRAgent:

    def __init__(self, api_key: Optional[str] = None):

        self.client = LLMClient
        self.model = "gemini-2.5-flash"

    def extract_text(self, file) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{file['content_type']};base64,{b64encode(file['content']).decode('utf-8')}",
                            },
                        },
                    ],
                },
                {
                    "role": "system",
                    "content": OCR_SYSTEM_INSTRUCTION,
                },
            ],
        )

        return response.choices[0].message.content
