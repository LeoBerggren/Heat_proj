from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.heat import Heat
from app.api.schemas import HeatCreate, HeatRead

router = APIRouter(prefix="/admin/heats", tags=["Admin Heats"])


@router.get("/", response_model=list[HeatRead])
def list_heats(db: Session = Depends(get_db)):
    return db.query(Heat).all()


@router.post("/", response_model=HeatRead)
def create_heat(data: HeatCreate, db: Session = Depends(get_db)):
    heat = Heat(
        round=data.round,
        start_time=data.start_time,
        end_time=data.end_time,
        status="pending"
    )
    db.add(heat)
    db.commit()
    db.refresh(heat)
    return heat


@router.delete("/{heat_id}")
def delete_heat(heat_id: int, db: Session = Depends(get_db)):
    heat = db.query(Heat).filter(Heat.id == heat_id).first()
    if not heat:
        raise HTTPException(status_code=404, detail="Heat not found")

    db.delete(heat)
    db.commit()
    return {"message": "Heat deleted"}
