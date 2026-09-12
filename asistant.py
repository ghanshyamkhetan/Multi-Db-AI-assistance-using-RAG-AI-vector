from metadata import build_schema_document
from sql_agent import generate_sql
from security import validate_sql
from db import execute_query
from llm import ask_llm

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

        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]

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

def answer_from_knowledge(question, knowledge):

    knowledge_text = ""

    for item in knowledge:

        knowledge_text += f"""
SOURCE: {item['source']}

CONTENT:
{item['content']}

-------------------------
"""

    prompt = f"""
You are a PostgreSQL DBA assistant.

Answer the user's question using ONLY the
approved DBA documentation and runbooks below.

Do not invent information.

If the answer is not available in the provided
documents, say so clearly.

APPROVED DBA KNOWLEDGE:

{knowledge_text}

USER QUESTION:

{question}

Give a clear and practical DBA answer.

Mention the source document used.
"""

    from llm import ask_llm

    return ask_llm(prompt)

# --------------------------------------------------
# MAIN DBA ASSISTANT
# --------------------------------------------------

def ask_database(question):

    print("\n\n******** DBA ASSISTANT CALLED ********")
    print("QUESTION:", question)
    print("**************************************\n")


    # ---------------------------------------------
    # 1. Retrieve knowledge using RAG
    # ---------------------------------------------

    knowledge = retrieve_knowledge(
        question
    )

    answer = answer_from_knowledge(
    question,
    knowledge
    )

    knowledge_text = ""

    for item in knowledge:
        knowledge_text += f"""
    SOURCE: {item['source']}

    CONTENT:
    {item['content']}

    -------------------------
    """

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
        schema,
        knowledge_text
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
    # 7. Return result
    # ---------------------------------------------

    return {
        "answer": answer,
        "sql": sql,
        "result": result,
        "knowledge": knowledge
    }