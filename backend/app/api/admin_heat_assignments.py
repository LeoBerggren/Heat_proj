from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.heat import Heat
from app.models.competitor import Competitor
from app.models.heat_competitor import HeatCompetitor

router = APIRouter(prefix="/admin/heats", tags=["Admin Heat Assignments"])

@router.get("/{heat_id}/competitors")
def get_heat_competitors(heat_id: int, db: Session = Depends(get_db)):
    assignments = (
        db.query(HeatCompetitor)
        .filter(HeatCompetitor.heat_id == heat_id)
        .all()
    )
    competitor_ids = [a.competitor_id for a in assignments]
    competitors = (
        db.query(Competitor)
        .filter(Competitor.id.in_(competitor_ids))
        .all()
    )
    return competitors


@router.post("/{heat_id}/competitors/{competitor_id}")
def add_competitor_to_heat(heat_id: int, competitor_id: int, db: Session = Depends(get_db)):
    # Check heat exists
    heat = db.query(Heat).filter(Heat.id == heat_id).first()
    if not heat:
        raise HTTPException(status_code=404, detail="Heat not found")

    # Check competitor exists
    competitor = db.query(Competitor).filter(Competitor.id == competitor_id).first()
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")

    # Check if already assigned
    existing = (
        db.query(HeatCompetitor)
        .filter(HeatCompetitor.heat_id == heat_id,
                HeatCompetitor.competitor_id == competitor_id)
        .first()
    )
    if existing:
        return {"message": "Already assigned"}

    assignment = HeatCompetitor(heat_id=heat_id, competitor_id=competitor_id)
    db.add(assignment)
    db.commit()

    return {"message": "Competitor added to heat"}


@router.delete("/{heat_id}/competitors/{competitor_id}")
def remove_competitor_from_heat(heat_id: int, competitor_id: int, db: Session = Depends(get_db)):
    assignment = (
        db.query(HeatCompetitor)
        .filter(HeatCompetitor.heat_id == heat_id,
                HeatCompetitor.competitor_id == competitor_id)
        .first()
    )
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    db.delete(assignment)
    db.commit()

    return {"message": "Competitor removed from heat"}
