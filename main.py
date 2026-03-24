from fastapi import FastAPI
from app.llm import generate_sql
from app.db import execute_query
from app.schema import schema

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Text-to-SQL API Running"}

@app.post("/query")
def query_db(question: str):
    try:
        sql_query = generate_sql(question, schema)
        result = execute_query(sql_query)

        return {
            "question": question,
            "sql": sql_query,
            "result": result
        }

    except Exception as e:
        return {"error": str(e)}