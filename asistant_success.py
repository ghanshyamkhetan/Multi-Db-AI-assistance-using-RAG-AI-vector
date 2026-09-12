from metadata import build_schema_document
from sql_agent import generate_sql
from security import validate_sql
from db import execute_query


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

def ask_database(question):

    schema = build_schema_document()

    sql = generate_sql(
        question,
        schema
    )

    # Clean LLM Markdown formatting
    sql = clean_sql(sql)

    print("\nGenerated SQL:")
    print(sql)

    # Validate SQL before execution
    validate_sql(sql)

    # Execute SQL
    result = execute_query(sql)

    return {
        "sql": sql,
        "result": result
    }