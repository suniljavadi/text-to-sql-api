from fastapi.testclient import TestClient

from main import app


def test_query_requires_configured_api_token(monkeypatch):
    monkeypatch.delenv("API_TOKEN", raising=False)

    response = TestClient(app).post("/query", params={"question": "show customers"})

    assert response.status_code == 503
    assert response.headers["X-Request-ID"]


def test_query_rejects_short_api_token(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "short-token")

    response = TestClient(app).post("/query", params={"question": "show customers"})

    assert response.status_code == 503


def test_query_rejects_invalid_api_token(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "expected-token" * 3)

    response = TestClient(app).post(
        "/query",
        params={"question": "show customers"},
        headers={"Authorization": "Bearer " + "wrong-token" * 3},
    )

    assert response.status_code == 401


def test_query_validates_question_length(monkeypatch):
    token = "expected-token" * 3
    monkeypatch.setenv("API_TOKEN", token)

    response = TestClient(app).post(
        "/query",
        params={"question": "x" * 2001},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422


def test_query_accepts_valid_token(monkeypatch):
    token = "expected-token" * 3
    monkeypatch.setenv("API_TOKEN", token)
    monkeypatch.setattr("main.generate_sql", lambda question, schema: "SELECT 1")
    monkeypatch.setattr("main.execute_query", lambda query: [{"value": 1}])

    response = TestClient(app).post(
        "/query",
        params={"question": "show one"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["result"] == [{"value": 1}]
