from fastapi import APIRouter, Depends, status, HTTPException, Query
from app.database import get_db
from typing import List, Optional
from app.schemas import bat
from sqlalchemy.orm import Session
from app.crud import BatService
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.dependencies.auth import require_admin
from app.utils.validators import parse_bool_param, parse_brand_param
router = APIRouter(
    prefix="/bats",
    tags=["Bats"],
    dependencies=[Depends(get_current_user)]
)

bat_service = BatService()

@router.get("/search", response_model=List[bat.Bat])
def search_bats(
    brand: str | None = None,
    is_wood: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    brand_clean = parse_brand_param(brand)
    is_wood_bool = parse_bool_param(is_wood, field_name="is_wood")
    return bat_service.search(db=db, brand=brand_clean, is_wood=is_wood_bool)


@router.post("/", response_model=bat.Bat, status_code=status.HTTP_201_CREATED)
def create_bat(bat: bat.BatCreate, db: Session = Depends(get_db)):
    return bat_service.create(db=db, obj_in=bat)

@router.get("/wood", response_model=List[bat.Bat])
def get_wood_bats(db: Session = Depends(get_db)):
    return bat_service.search(db=db, is_wood=True)

@router.get("/metal", response_model=List[bat.Bat])
def get_metal_bats(db: Session = Depends(get_db)):
    return bat_service.search(db=db, is_wood=False)

@router.get("/{bat_id}", response_model=bat.Bat)
def get_bat(bat_id: int, db: Session = Depends(get_db)):
    bat = bat_service.get(db=db, obj_id=bat_id)
    if not bat:
        raise HTTPException(status_code=404, detail="Bat not found")
    return bat
@router.put("/{bat_id}", response_model=bat.Bat)
def update_bat(bat_id: int, bat_update: bat.BatCreate, db: Session = Depends(get_db)):
    existing = bat_service.get(db=db, obj_id=bat_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Bat not found")
    return bat_service.update(db=db, db_obj=existing, obj_in=bat_update)

@router.delete("/{bat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bat(bat_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    existing = bat_service.get(db=db, obj_id=bat_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Bat not found")
    return bat_service.remove(db=db, obj_id=bat_id)
