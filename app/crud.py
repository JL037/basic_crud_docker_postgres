from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.schemas import bat
from app.models import bats
from app.utils.validators import parse_sort
from app.utils.decorators import timed_crud
class BatService:

    @timed_crud
    def search(self, db: Session, brand: str | None = None, is_wood: bool | None = None, skip: int = 0, limit: int = 10,
                min_price: float | None = None, max_price: float | None = None, order_by: str = "price", order_dir: str = "asc"):
        query = db.query(bats.Bat)

        if brand is not None:
            query = query.filter(bats.Bat.brand.ilike(f"%{brand}%"))

        if is_wood is not None:
            query = query.filter(bats.Bat.is_wood == is_wood)

        if min_price is not None:
            query = query.filter(bats.Bat.price >= min_price)

        if max_price is not None:
            query = query.filter(bats.Bat.price <= max_price)

        column_expr = parse_sort(order_by, order_dir)
        query = query.order_by(column_expr)

        
        print("Ordering by:", order_by, "Direction:", order_dir)
        

        results = query.offset(skip).limit(limit).all()
        print("Filtered IDs:", [bat.id for bat in results])
        return results
    
    @timed_crud
    def create(self, db: Session, obj_in: bat.BatCreate):
        db_bat = bats.Bat(**obj_in.model_dump())
        db.add(db_bat)
        db.commit()
        db.refresh(db_bat)
        return db_bat
    
    @timed_crud
    def get(self, db: Session, obj_id: int):
        return db.query(bats.Bat).filter(bats.Bat.id == obj_id).first()
    
    @timed_crud
    def update(self, db: Session, db_obj: bats.Bat, obj_in: bat.BatCreate):
        data = obj_in.model_dump()
        ALLOWED_UPDATE_FIELDS = ["name", "brand", "price", "is_wood"]

        for field, value in data.items():
            if field in ALLOWED_UPDATE_FIELDS:
                setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    @timed_crud
    def remove(self, db: Session, obj_id: int):
        db_obj = db.query(bats.Bat).filter(bats.Bat.id == obj_id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()