from metadata import build_schema_document
from sql_agent import generate_sql
from security import validate_sql
from db import execute_query

from rag import (
    load_documents,
    split_documents,
    add_database_schema,
    create_vector_store
)


# --------------------------------------------------
# SQL CLEANING
# --------------------------------------------------

def clean_sql(sql):

    sql = sql.strip()

    if sql.startswith("```"):

        lines = sql.splitlines()

        # Remove opening ```sql / ```
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]

        # Remove closing ```
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        sql = "\n".join(lines)

    return sql.strip()


# --------------------------------------------------
# BUILD RAG VECTOR STORE
# --------------------------------------------------

def build_rag():

    documents = load_documents()

    documents = add_database_schema(
        documents
    )

    chunks = split_documents(
        documents
    )

    vector_store = create_vector_store(
        chunks
    )

    return vector_store


# --------------------------------------------------
# RETRIEVE DBA KNOWLEDGE
# --------------------------------------------------

def retrieve_knowledge(question):

    vector_store = build_rag()

    results = vector_store.similarity_search(
        question,
        k=3
    )

    knowledge = []

    for doc in results:

        knowledge.append({
            "source": doc.metadata.get("source"),
            "content": doc.page_content
        })

    return knowledge


# --------------------------------------------------
# MAIN DBA ASSISTANT
# --------------------------------------------------

def ask_database(question):

    # ---------------------------------------------
    # 1. Retrieve DBA knowledge using RAG
    # ---------------------------------------------

    knowledge = retrieve_knowledge(
        question
    )

    print("\n====================================")
    print("RAG KNOWLEDGE")
    print("====================================")

    for item in knowledge:

        print("\nSOURCE:")
        print(item["source"])

        print("\nCONTENT:")
        print(item["content"])


    # ---------------------------------------------
    # 2. Get live database schema
    # ---------------------------------------------

    schema = build_schema_document()


    # ---------------------------------------------
    # 3. Generate SQL
    # ---------------------------------------------

    sql = generate_sql(
        question,
        schema
    )


    # ---------------------------------------------
    # 4. Clean SQL
    # ---------------------------------------------

    sql = clean_sql(
        sql
    )


    print("\nGenerated SQL:")
    print(sql)


    # ---------------------------------------------
    # 5. Validate SQL
    # ---------------------------------------------

    validate_sql(
        sql
    )


    # ---------------------------------------------
    # 6. Execute SQL
    # ---------------------------------------------

    result = execute_query(
        sql
    )


    # ---------------------------------------------
    # 7. Return everything
    # ---------------------------------------------

    return {
        "sql": sql,
        "result": result,
        "knowledge": knowledge
    }