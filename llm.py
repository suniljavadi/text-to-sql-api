from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def generate_sql(question, schema):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured")
    client = OpenAI(api_key=api_key)
    prompt = f"""
You are a SQL expert.

Convert the following natural language question into SQL query.

Schema:
{schema}

Question:
{question}

Only return SQL query.
"""

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()