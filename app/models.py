from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text, String, Float, Boolean
from app.database import Base

class Bat(Base):
    __tablename__ = "bats"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    brand: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    is_wood: Mapped[bool] = mapped_column(Boolean, nullable=False)