import pyodbc
import os
import re
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    connection_string = os.getenv("DB_CONNECTION")
    if not connection_string:
        raise RuntimeError("DB_CONNECTION is not configured")
    conn = pyodbc.connect(connection_string)
    return conn


def validate_read_only_sql(query):
    normalized = query.strip()
    if not normalized:
        raise ValueError("Generated SQL is empty")
    if not re.match(r"^(SELECT|WITH)\b", normalized, re.IGNORECASE):
        raise ValueError("Only read-only SELECT or WITH queries are allowed")
    if ";" in normalized or "--" in normalized or "/*" in normalized:
        raise ValueError("Comments and multiple SQL statements are not allowed")
    if re.search(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|MERGE|EXEC|CREATE)\b", normalized, re.IGNORECASE):
        raise ValueError("Mutation and administrative SQL is not allowed")
    return normalized

def execute_query(query):
    validate_read_only_sql(query)
    conn = get_connection()
    try:
        cursor = conn.cursor()
        timeout_seconds = int(os.getenv("QUERY_TIMEOUT_SECONDS", "15"))
        max_result_rows = int(os.getenv("MAX_RESULT_ROWS", "1000"))
        if timeout_seconds < 1 or max_result_rows < 1:
            raise RuntimeError("Query timeout and maximum result rows must be positive")
        cursor.timeout = timeout_seconds
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchmany(max_result_rows + 1)
        if len(rows) > max_result_rows:
            raise ValueError(f"Query exceeded the maximum result size of {max_result_rows} rows")
        return [dict(zip(columns, row)) for row in rows]
    finally:
        conn.close()