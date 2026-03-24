import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn = pyodbc.connect(os.getenv("DB_CONNECTION"))
    return conn

def execute_query(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)

    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append(dict(zip(columns, row)))

    conn.close()
    return result