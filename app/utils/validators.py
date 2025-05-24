from fastapi import HTTPException
from app.models import bats

ALLOWED_ORDER_FIELDS = ["price", "brand", "id", "name"]


def parse_bool_param(value: str | None, field_name: str = "value") -> bool | None:
    if value is None:
        return None
    value = value.strip().lower()
    if value in {"true", "1"}:
        return True
    elif value in {"false", "0"}:
        return False
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid boolean for '{field_name}'. Use true/false or 1/0."
        )
    

def parse_brand_param(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip().title()
    if not value or len(value) < 2:
        raise HTTPException(status_code=400, detail="Brand must be at least 2 characters")
    return value


def normalize_brand(value: str) -> str:
    value = value.strip().title()
    if len(value) < 2:
        raise ValueError("Brand must be at least 2 characters long.")
    return value


def clean_bat_name(value: str) -> str:
    value = value.strip()

    if not value:
        raise ValueError("Bat name cannot be empty or just whitespace.")

    if not value.replace(" ", "").replace("-", "").isalnum():
        raise ValueError("Bat name contains invalid characters.")

    return value

def validate_order_by(value: str, allowed_fields: list[str]) -> str:
    if value not in allowed_fields:
        raise HTTPException(status_code=400, detail=f"Invalid order_by field: {value}")
    return value


def validate_order_dir(value: str) -> str:
    if value.lower() not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="order_dir must be 'asc' or 'desc'")
    return value.lower()


def parse_filters(brand, is_wood, order_by, order_dir):
    return {
        "brand": parse_brand_param(brand),
        "is_wood": parse_bool_param(is_wood, field_name="is_wood"),
        "order_by": validate_order_by(order_by, ALLOWED_ORDER_FIELDS),
        "order_dir": validate_order_dir(order_dir),
    }

def parse_sort(order_by: str, order_dir: str):
    if order_by not in ALLOWED_ORDER_FIELDS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid order_by field: '{order_by}'. Must be one of {ALLOWED_ORDER_FIELDS}"
        )

    column = getattr(bats.Bat, order_by)

    if order_dir == "desc":
        return column.desc()
    elif order_dir == "asc":
        return column.asc()
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid order_dir. Must be 'asc' or 'desc'."
        )