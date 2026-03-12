import os
from dotenv import load_dotenv
from requests import Session
from .instructions import systemt_instructions
from core.llm_client import client as LLMClient
from agents.ocr_agent.agent import OCRAgent
from PyPDF2 import PdfReader
import io
from pydantic import BaseModel

from services import case_service
from core.s3 import s3
from pydantic import BaseModel, Field
from core.database import engine
from sqlmodel import Session

from helpers.docx import convert_text_to_docx

load_dotenv()


class ResponseModel(BaseModel):
    description: str = ""
    parties_and_attorneys: str = ""
    key_dates: str = ""
    assets_disclosed: str = ""
    income_and_expenses: str = ""
    claims_and_disputed_items: str = ""
    key_findings_and_observations: str = ""
    flagged_inconsistencies: str = ""


class SummarizerAgent:
    def extract_text(self, file_urls):
        files = []
        for url in file_urls:
            response = s3.get_object(Bucket="casebot", Key=url.split("/")[-1])
            file_content = response["Body"].read()
            content_type = response["ContentType"]
            files.append({"content": file_content, "content_type": content_type})
        text = ""

        for file in files:
            file["content"] = io.BytesIO(file["content"])

            if file["content_type"].startswith("image/"):
                text += OCRAgent().extract_text(file["content"])

            elif file["content_type"] == "application/pdf":
                pdf = PdfReader(file["content"])

                for page in pdf.pages:
                    text += page.extract_text() or ""

            elif file["content_type"] == "text/plain":
                text += file["content"].read().decode("utf-8")
        return text

    async def run(self, file_urls, case_id):
        text = await self.extract_text(file_urls)

        messages = [
            {"role": "system", "content": systemt_instructions},
            {
                "role": "user",
                "content": f"Here are the case documents and images: {text}",
            },
        ]

        response = (
            LLMClient.chat.completions.parse(
                model="gemini-2.5-flash",
                messages=messages,
                max_tokens=4000,
                response_format=ResponseModel,
            )
            .choices[0]
            .message.parsed
        )

        file_stream = convert_text_to_docx(response)

        with Session(engine) as session:
            case_service.upload_case_summary(
                file_stream=file_stream,
                case_id=case_id,
                response=response,
                session=session,
            )
        return response
