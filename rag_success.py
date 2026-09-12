from langchain_core.documents import Document
from metadata import build_schema_document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

import os
from config import GOOGLE_API_KEY

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2"
)


def load_documents():

    documents = []

    pdf_loader = PyPDFLoader(
        "knowledge/postgres/postgres_admin.pdf"
    )

    documents.extend(pdf_loader.load())

    txt_loader = TextLoader(
        "knowledge/runbooks/high_cpu.md"
    )

    documents.extend(txt_loader.load())

    return documents


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    return splitter.split_documents(documents)

def add_database_schema(documents):

    schema_text = build_schema_document()

    schema_doc = Document(
        page_content=schema_text,
        metadata={
            "source": "postgresql_database",
            "type": "database_schema"
        }
    )

    documents.append(schema_doc)

    return documents