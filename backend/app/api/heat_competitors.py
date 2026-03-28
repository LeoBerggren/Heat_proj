from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.heat_competitor import HeatCompetitor
from app.api.schemas import HeatCompetitorCreate, HeatCompetitorRead

router = APIRouter()

# CREATE (assign competitor to heat)
@router.post("/heat-competitors", response_model=HeatCompetitorRead)
def assign_competitor(data: HeatCompetitorCreate, db: Session = Depends(get_db)):
    assignment = HeatCompetitor(
        heat_id=data.heat_id,
        competitor_id=data.competitor_id
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

# READ ALL
@router.get("/heat-competitors", response_model=list[HeatCompetitorRead])
def list_assignments(db: Session = Depends(get_db)):
    return db.query(HeatCompetitor).all()

# READ ONE
@router.get("/heat-competitors/{assignment_id}", response_model=HeatCompetitorRead)
def get_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(HeatCompetitor).filter(HeatCompetitor.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

# DELETE (remove competitor from heat)
@router.delete("/heat-competitors/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(HeatCompetitor).filter(HeatCompetitor.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    db.delete(assignment)
    db.commit()
    return {"status": "deleted"}
