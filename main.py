from fastapi import FastAPI
from fastapi import HTTPException

from db import execute_query, validate_read_only_sql
from llm import generate_sql
from schema import schema

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Text-to-SQL API Running"}

@app.post("/query")
def query_db(question: str):
    try:
        sql_query = generate_sql(question, schema)
        validate_read_only_sql(sql_query)
        result = execute_query(sql_query)

        return {
            "question": question,
            "sql": sql_query,
            "result": result
        }

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Query processing failed") from exc