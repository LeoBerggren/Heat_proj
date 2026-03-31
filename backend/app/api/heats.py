from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.heat import Heat
from app.api.schemas import HeatCreate, HeatRead
from app.models.heat_competitor import HeatCompetitor
from app.models.competitor import Competitor


router = APIRouter()

# CREATE
@router.post("/heats", response_model=HeatRead)
def create_heat(data: HeatCreate, db: Session = Depends(get_db)):
    heat = Heat(
        event_id=data.event_id,
        round=data.round,
        start_time=data.start_time,
        end_time=data.end_time,
        status=data.status
    )
    db.add(heat)
    db.commit()
    db.refresh(heat)
    return heat

#Gets heat competitors
@router.get("/heats/{heat_id}/competitors")
def get_competitors_in_heat(heat_id: int, db: Session = Depends(get_db)):
    competitors = (
        db.query(Competitor)
        .join(HeatCompetitor, HeatCompetitor.competitor_id == Competitor.id)
        .filter(HeatCompetitor.heat_id == heat_id)
        .all()
    )

    return competitors

# READ ALL
@router.get("/heats", response_model=list[HeatRead])
def list_heats(db: Session = Depends(get_db)):
    return db.query(Heat).all()

# READ ONE
@router.get("/heats/{heat_id}", response_model=HeatRead)
def get_heat(heat_id: int, db: Session = Depends(get_db)):
    heat = db.query(Heat).filter(Heat.id == heat_id).first()
    if not heat:
        raise HTTPException(status_code=404, detail="Heat not found")
    return heat

# UPDATE
@router.put("/heats/{heat_id}", response_model=HeatRead)
def update_heat(heat_id: int, data: HeatCreate, db: Session = Depends(get_db)):
    heat = db.query(Heat).filter(Heat.id == heat_id).first()
    if not heat:
        raise HTTPException(status_code=404, detail="Heat not found")

    heat.event_id = data.event_id
    heat.round = data.round
    heat.start_time = data.start_time
    heat.end_time = data.end_time
    heat.status = data.status

    db.commit()
    db.refresh(heat)
    return heat

# DELETE
@router.delete("/heats/{heat_id}")
def delete_heat(heat_id: int, db: Session = Depends(get_db)):
    heat = db.query(Heat).filter(Heat.id == heat_id).first()
    if not heat:
        raise HTTPException(status_code=404, detail="Heat not found")

    db.delete(heat)
    db.commit()
    return {"status": "deleted"}
