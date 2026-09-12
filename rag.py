from langchain_core.documents import Document

from metadata import build_schema_document

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_postgres import PGVector

import os

from config import GOOGLE_API_KEY, DB_CONFIG


os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2"
)


def load_documents():

    documents = []

    pdf_loader = PyPDFLoader(
        "knowledge/postgres/postgres_admin.pdf"
    )

    documents.extend(
        pdf_loader.load()
    )

    txt_loader = TextLoader(
        "knowledge/runbooks/high_cpu.md"
    )

    documents.extend(
        txt_loader.load()
    )

    return documents


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


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    return splitter.split_documents(
        documents
    )


def get_connection_string():

    return (
        f"postgresql+psycopg://"
        f"{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}"
        f"/{DB_CONFIG['dbname']}"
    )


def create_vector_store(documents):

    connection = get_connection_string()

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name="dba_knowledge",
        connection=connection,
        use_jsonb=True,
    )

    vector_store.add_documents(
        documents
    )

    return vector_store