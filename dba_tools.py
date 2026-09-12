def get_long_running_queries():

    sql = """
    SELECT
        pid,
        usename,
        now() - query_start AS duration,
        state,
        query
    FROM pg_stat_activity
    WHERE query_start IS NOT NULL
      AND now() - query_start > interval '5 minutes'
    ORDER BY duration DESC;
    """

    return execute_query(sql)

def get_database_size():

    sql = """
    SELECT
        pg_size_pretty(
            pg_database_size(current_database())
        ) AS database_size;
    """

    return execute_query(sql)

def get_active_sessions():

    sql = """
    SELECT
        pid,
        usename,
        state,
        query_start,
        query
    FROM pg_stat_activity
    WHERE state <> 'idle'
    ORDER BY query_start;
    """

    return execute_query(sql)