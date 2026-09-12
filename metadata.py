from db import execute_query


def get_tables():
    sql = """
    SELECT
        table_schema,
        table_name
    FROM information_schema.tables
    WHERE table_type = 'BASE TABLE'
      AND table_schema NOT IN ('pg_catalog', 'information_schema')
    ORDER BY table_schema, table_name;
    """

    return execute_query(sql)


def get_columns():
    sql = """
    SELECT
        table_schema,
        table_name,
        column_name,
        data_type
    FROM information_schema.columns
    WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
    ORDER BY table_schema, table_name, ordinal_position;
    """

    return execute_query(sql)


def build_schema_document():
    tables = get_tables()
    columns = get_columns()

    document = "POSTGRESQL DATABASE SCHEMA\n\n"

    for table in tables:
        schema = table["table_schema"]
        table_name = table["table_name"]

        document += f"Schema: {schema}\n"
        document += f"Table: {table_name}\n"

        for column in columns:
            if (
                column["table_schema"] == schema
                and column["table_name"] == table_name
            ):
                document += (
                    f"  Column: {column['column_name']} "
                    f"Type: {column['data_type']}\n"
                )

        document += "\n"

    return document