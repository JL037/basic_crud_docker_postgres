from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import models, schemas

class BatService:
    def search(self, db: Session, brand: str | None = None, is_wood: bool | None = None):
        query = db.query(models.Bat)

        if brand is not None:
            query = query.filter(models.Bat.brand.ilike(f"%{brand}%"))

        if is_wood is not None:
            query = query.filter(models.Bat.is_wood == is_wood)

        return query.all()
    
    def create(self, db: Session, obj_in: schemas.BatCreate):
        db_bat = models.Bat(**obj_in.model_dump())
        db.add(db_bat)
        db.commit()
        db.refresh(db_bat)
        return db_bat

    def get(self, db: Session, obj_id: int):
        return db.query(models.Bat).filter(models.Bat.id == obj_id).first()
    
    def update(self, db: Session, db_obj: models.Bat, obj_in: schemas.BatCreate):
        data = obj_in.model_dump()
        for field, value in data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, obj_id: int):
        db_obj = db.query(models.Bat).filter(models.Bat.id == obj_id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()