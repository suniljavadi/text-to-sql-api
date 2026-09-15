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