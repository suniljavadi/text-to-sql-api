# Text-to-SQL API Prototype

**Status: Experimental prototype**

A small Python/FastAPI prototype for converting natural-language questions into SQL and executing the result against a configured database. The repository contains `main.py`, `llm.py`, `db.py`, and `schema.py`; it is a smaller predecessor or companion experiment to the more complete [Enterprise Text-to-SQL AI Agent](https://github.com/suniljavadi/Text-to-SQL-AI-Agent).

## Architecture

```mermaid
flowchart LR
  U[User] --> A[FastAPI application]
  A --> L[LLM adapter]
  L --> Q[Generated SQL]
  Q --> D[Database helper]
  D --> R[Response]
```

## Repository Structure

- `main.py`: FastAPI entry point and routes.
- `llm.py`: LLM interaction boundary.
- `db.py`: database access helper.
- `schema.py`: schema/model definitions.

## Technology Scope

Python, FastAPI, LLM integration, `pyodbc` database access, and environment-based configuration are evidenced by the source files. `requirements.txt`, `.env.example`, and focused read-only SQL tests are included; Docker configuration and a database fixture are not included.

## Local Exploration

Create a virtual environment, install the dependencies, configure the database, model credentials, and optional schema context outside source control, then run the FastAPI entry point:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Set `OPENAI_API_KEY`, `DB_CONNECTION`, and optionally `DB_SCHEMA` in `.env`. The application imports successfully without an API key, but requests fail clearly until the key is configured. No production deployment is claimed.

## Safety Boundary

Generated SQL is validated before execution. Only single read-only `SELECT` or `WITH` statements are accepted; comments, multiple statements, mutation keywords, and administrative SQL are rejected. Database connections are closed in a `finally` block, and API failures return controlled HTTP errors instead of raw exception details.

Run the focused tests with:

```bash
pytest -q
```

## Security and Limitations

Generated SQL should be treated as untrusted text. The current guard permits only single read-only `SELECT` or `WITH` statements and rejects comments, multiple statements, mutations, and administrative SQL. Before connecting this prototype to real data, add row limits, timeout handling, authentication, and audit logging. Do not place API keys or database passwords in source files.

## Future Improvements

Add database fixtures, a formal SQL parser, structured API schemas, query timeout enforcement, authentication, and an evaluation set that separates SQL validity from execution and semantic correctness.

## Resume Relevance

Demonstrates early-stage Python, FastAPI, LLM integration, database interaction, and the problem framing behind the larger Text-to-SQL engineering project.

## Author

**Sunil Javadi**

- [GitHub](https://github.com/suniljavadi)
- [Portfolio](https://github.com/suniljavadi/sunil-portfolio)
- [LinkedIn](https://www.linkedin.com/in/sunil-javadi/)
