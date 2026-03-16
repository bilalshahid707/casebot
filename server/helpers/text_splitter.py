from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from helpers.document_parser import parse_file_to_documents


def text_splitter(file) -> List[str]:

    # Parsing documents to get content according to pages and source
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
