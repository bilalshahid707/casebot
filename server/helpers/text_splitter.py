from typing import List
import io

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from agents.ocr_agent.agent import OCRAgent
from helpers.document_parser import parse_file_to_documents


def text_splitter(file) -> List[str]:

    parsed_documents = parse_file_to_documents(file)
    langchain_docs = []

    # print(parsed_documents)
    for doc in parsed_documents:
        langchain_docs.append(
            Document(
                page_content=doc.page_content,
                metadata=doc.model_dump(exclude={"page_content"}, exclude_none=True),
            )
        )

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_documents(langchain_docs)
    return chunks
