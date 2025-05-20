from fastapi import APIRouter, Depends, status, HTTPException
from app.database import get_db
from typing import List, Optional
from app import schemas
from sqlalchemy.orm import Session
from app.crud import BatService

router = APIRouter(
    prefix="/bats",
    tags=["Bats"]
)

bat_service = BatService()

@router.get("/search", response_model=List[schemas.Bat])
def search_bats(
    brand: Optional[str] = None,
    is_wood: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    return bat_service.search(db=db, brand=brand, is_wood=is_wood)

@router.post("/", response_model=schemas.Bat, status_code=status.HTTP_201_CREATED)
def create_bat(bat: schemas.BatCreate, db: Session = Depends(get_db)):
    return bat_service.create(db=db, obj_in=bat)

router.get("/{bat_id}", response_model=schemas.Bat)
def get_bat(bat_id: int, db: Session = Depends(get_db)):
    bat = bat_service.get(db=db, obj_id=bat_id)
    if not bat:
        raise HTTPException(status_code=404, detail="Bat not found")
    return bat

router.get("/wood", response_model=List[schemas.Bat])
def get_wood_bats(db: Session = Depends(get_db)):
    return bat_service.search(db=db, is_wood=True)

@router.get("/metal", response_model=List[schemas.Bat])
def get_metal_bats(db: Session = Depends(get_db)):
    return bat_service.search(db=db, is_wood=False)

@router.put("/{bat_id}", response_model=schemas.Bat)
def update_bat(bat_id: int, bat_update: schemas.BatCreate, db: Session = Depends(get_db)):
    existing = bat_service.get(db=db, obj_id=bat_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Bat not found")
    return bat_service.update(db=db, db_obj=existing, obj_in=bat_update)

@router.delete("/{bat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bat(bat_id: int, db: Session = Depends(get_db)):
    existing = bat_service.get(db=db, obj_id=bat_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Bat not found")
    return bat_service.remove(db=db, obj_id=bat_id)