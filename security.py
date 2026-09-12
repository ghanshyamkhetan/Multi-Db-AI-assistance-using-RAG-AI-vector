import re


FORBIDDEN = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE"
]


def validate_sql(sql):

    cleaned = sql.strip().upper()

    if not cleaned.startswith("SELECT"):
        raise ValueError(
            "Only SELECT queries are allowed."
        )

    for keyword in FORBIDDEN:

        pattern = rf"\b{keyword}\b"

        if re.search(pattern, cleaned):

            raise ValueError(
                f"Forbidden SQL operation: {keyword}"
            )

    return True