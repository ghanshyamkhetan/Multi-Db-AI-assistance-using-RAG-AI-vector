from llm import ask_llm


def generate_sql(question, schema, knowledge_text):

    prompt = f"""
You are a PostgreSQL DBA assistant.

You have access to:

1. Live PostgreSQL database schema
2. Approved DBA documentation
3. DBA troubleshooting runbooks

Use the DBA documentation and runbooks as guidance when
understanding the user's request.

Approved DBA knowledge:

{knowledge_text}

Database schema:

{schema}

User question:

{question}

Generate ONLY a PostgreSQL SELECT query.

Rules:

1. Only SELECT statements.
2. Do not modify data.
3. Do not create or drop objects.
4. Do not access system tables unless required.
5. Use the database schema provided above.
6. Use the DBA knowledge when it is relevant.
7. Do not invent tables or columns.
8. Return only SQL.
"""

    return ask_llm(prompt)