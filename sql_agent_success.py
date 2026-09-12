from llm import ask_llm


def generate_sql(question, schema):

    prompt = f"""
You are a PostgreSQL DBA assistant.

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
5. Return only SQL.
"""

    return ask_llm(prompt)