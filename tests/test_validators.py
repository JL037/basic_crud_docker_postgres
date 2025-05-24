import pytest
from fastapi import HTTPException
from sqlalchemy.sql.elements import ColumnElement
from app.utils.validators import parse_sort

def test_parse_sort_valid_fields():
    column = parse_sort("price", "asc")
    assert isinstance(column, ColumnElement)
    assert "price" in str(column)
    assert "ASC" in str(column)

    column = parse_sort("id", "desc")
    assert isinstance(column, ColumnElement)
    assert "id" in str(column)
    assert "DESC" in str(column)

def test_parse_sort_invalid_field():
    with pytest.raises(HTTPException, match="Invalid order_by field"):
        parse_sort("invalid_field", "asc")

def test_parse_sort_invalid_direction():
    with pytest.raises(HTTPException, match="Invalid order_dir"):
        parse_sort("price", "upwards")

