from pydantic import BaseModel

class BatBase(BaseModel):
    name: str
    brand: str
    price: float
    is_wood: bool

class BatCreate(BatBase):
    pass

class Bat(BatBase):
    id: int

    model_config = {
        "from_attributes": True
    }