from unittest.mock import Mock

import pytest

import db
from db import validate_read_only_sql


def test_allows_select_query():
    assert validate_read_only_sql("SELECT TOP 5 * FROM customers")


def test_rejects_mutation_query():
    try:
        validate_read_only_sql("DELETE FROM customers")
    except ValueError as exc:
        assert "read-only" in str(exc)
    else:
        raise AssertionError("Mutation query was accepted")


def test_rejects_multiple_statements():
    try:
        validate_read_only_sql("SELECT 1; DROP TABLE customers")
    except ValueError as exc:
        assert "statements" in str(exc)
    else:
        raise AssertionError("Multiple statements were accepted")


def test_execute_query_applies_timeout_and_row_limit(monkeypatch):
    cursor = Mock()
    cursor.description = [("value",)]
    cursor.fetchmany.return_value = [(1,), (2,)]
    connection = Mock()
    connection.cursor.return_value = cursor
    monkeypatch.setattr(db, "get_connection", lambda: connection)
    monkeypatch.setenv("QUERY_TIMEOUT_SECONDS", "5")
    monkeypatch.setenv("MAX_RESULT_ROWS", "2")

    assert db.execute_query("SELECT 1") == [{"value": 1}, {"value": 2}]
    assert cursor.timeout == 5
    cursor.fetchmany.assert_called_once_with(3)
    connection.close.assert_called_once()


def test_execute_query_rejects_results_over_row_limit(monkeypatch):
    cursor = Mock()
    cursor.description = [("value",)]
    cursor.fetchmany.return_value = [(1,), (2,), (3,)]
    connection = Mock()
    connection.cursor.return_value = cursor
    monkeypatch.setattr(db, "get_connection", lambda: connection)
    monkeypatch.setenv("QUERY_TIMEOUT_SECONDS", "5")
    monkeypatch.setenv("MAX_RESULT_ROWS", "2")

    with pytest.raises(ValueError, match="maximum result size"):
        db.execute_query("SELECT 1")
    connection.close.assert_called_once()