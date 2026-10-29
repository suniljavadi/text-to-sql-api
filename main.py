import hmac
import logging
import os
import time
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response

from db import execute_query, validate_read_only_sql
from llm import generate_sql
from schema import schema

app = FastAPI(title="Text-to-SQL API")
logger = logging.getLogger(__name__)


@app.middleware("http")
async def observe_requests(
    request: Request,
    call_next: RequestResponseEndpoint,
) -> Response:
    request_id = str(uuid4())
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        logger.exception(
            "http_request_failed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
            },
        )
        raise

    duration_ms = round((time.perf_counter() - started) * 1000, 2)
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "http_request_completed",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        },
    )
    return response


def require_api_token(authorization: str | None = Header(default=None)) -> None:
    expected_token = os.getenv("API_TOKEN")
    if not expected_token or len(expected_token) < 32:
        raise HTTPException(
            status_code=503,
            detail="API authentication is not configured with a strong token",
        )

    scheme, separator, supplied_token = (authorization or "").partition(" ")
    if (
        not separator
        or scheme.casefold() != "bearer"
        or not hmac.compare_digest(
            supplied_token.encode("utf-8"),
            expected_token.encode("utf-8"),
        )
    ):
        raise HTTPException(status_code=401, detail="Invalid or missing bearer token")


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "Text-to-SQL API Running"}


@app.post("/query")
def query_db(
    question: str = Query(..., min_length=1, max_length=2000),
    _: None = Depends(require_api_token),
) -> dict[str, object]:
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