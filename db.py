import psycopg
from config import DB_CONFIG


def get_connection():
    return psycopg.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )


def execute_query(sql):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)

            if cur.description is None:
                return []

            columns = [desc.name for desc in cur.description]

            rows = cur.fetchall()

            return [
                dict(zip(columns, row))
                for row in rows
            ]