from fastapi import HTTPException

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
