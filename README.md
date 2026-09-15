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

Python, FastAPI, LLM integration, and database access are evidenced by the source files. The repository does not include a `requirements.txt`, Docker configuration, test suite, or documented database schema, so exact dependency and deployment commands must be confirmed before use.

## Local Exploration

Create a virtual environment, install the dependencies required by the imports in the source files, configure the database and model credentials outside source control, then run the FastAPI entry point after confirming the application object name in `main.py`:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install fastapi uvicorn
uvicorn main:app --reload
```

The command assumes `main.py` exposes an ASGI object named `app`; verify the file before running. No production deployment is claimed.

## Security and Limitations

Generated SQL should be treated as untrusted text. Before connecting this prototype to real data, add read-only credentials, SQL parsing and allow-list validation, row limits, timeout handling, input/output validation, authentication, audit logging, and tests. Do not place API keys or database passwords in source files.

## Future Improvements

Add a dependency manifest, `.env.example`, schema-aware retrieval, safe SQL validation, structured API schemas, error handling, tests, database fixtures, and an evaluation set that separates SQL validity from execution and semantic correctness.

## Resume Relevance

Demonstrates early-stage Python, FastAPI, LLM integration, database interaction, and the problem framing behind the larger Text-to-SQL engineering project.

## Author

**Sunil Javadi**

- [GitHub](https://github.com/suniljavadi)
- [Portfolio](https://github.com/suniljavadi/sunil-portfolio)
- [LinkedIn](https://www.linkedin.com/in/sunil-javadi/)
