from typing import List
import io

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from agents.ocr_agent.agent import OCRAgent


async def text_splitter(file) -> List[str]:

    docs = []

    if file["content_type"].startswith("image/"):
        text = await OCRAgent().extract_text(file)
        docs.append(Document(page_content=text, metadata={"source": file["filename"]}))

    elif file["content_type"] == "application/pdf":
        pdf = PdfReader(io.BytesIO(file["content"]))
        for i in range(len(pdf.pages)):
            docs.append(
                Document(
                    page_content=pdf.pages[i].extract_text() or "",
                    metadata={"source": file["filename"], "page": i + 1},
                )
            )

    elif file["content_type"] in (
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ):
        docx = DocxDocument(io.BytesIO(file["content"]))
        for i, para in enumerate(docx.paragraphs):
            if para.text.strip():
                docs.append(
                    Document(
                        page_content=para.text,
                        metadata={"source": file["filename"]},
                    )
                )

    elif file["content_type"] in ("text/plain", "text/markdown"):
        text = file["content"].decode("utf-8")
        docs.append(Document(page_content=text, metadata={"source": file["filename"]}))

    else:
        raise ValueError(f"Unsupported file type: {file['content_type']}")

    if not docs:
        raise ValueError("No text extracted from file")

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_documents(docs)
    return chunks
