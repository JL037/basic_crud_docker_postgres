from pydantic import BaseModel, field_validator
from app.utils.validators import normalize_brand, clean_bat_name

class BatBase(BaseModel):
    name: str
    brand: str
    price: float
    is_wood: bool

class BatCreate(BatBase):
    brand: str

    @field_validator("brand")
    @classmethod
    def clean_brand(cls, value: str) -> str:
        return normalize_brand(value)
    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        return clean_bat_name(value)

class Bat(BatBase):
    id: int

    model_config = {
        "from_attributes": True
    }