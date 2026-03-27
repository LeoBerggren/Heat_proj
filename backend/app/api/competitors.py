from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.competitor import Competitor
from app.api.schemas import CompetitorCreate, CompetitorRead

router = APIRouter()

# CREATE
@router.post("/competitors", response_model=CompetitorRead)
def create_competitor(data: CompetitorCreate, db: Session = Depends(get_db)):
    competitor = Competitor(name=data.name, country=data.country)
    db.add(competitor)
    db.commit()
    db.refresh(competitor)
    return competitor

# READ ALL
@router.get("/competitors", response_model=list[CompetitorRead])
def list_competitors(db: Session = Depends(get_db)):
    return db.query(Competitor).all()

# READ ONE
@router.get("/competitors/{competitor_id}", response_model=CompetitorRead)
def get_competitor(competitor_id: int, db: Session = Depends(get_db)):
    competitor = db.query(Competitor).filter(Competitor.id == competitor_id).first()
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    return competitor

# UPDATE
@router.put("/competitors/{competitor_id}", response_model=CompetitorRead)
def update_competitor(competitor_id: int, data: CompetitorCreate, db: Session = Depends(get_db)):
    competitor = db.query(Competitor).filter(Competitor.id == competitor_id).first()
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")

    competitor.name = data.name
    competitor.country = data.country

    db.commit()
    db.refresh(competitor)
    return competitor

# DELETE
@router.delete("/competitors/{competitor_id}")
def delete_competitor(competitor_id: int, db: Session = Depends(get_db)):
    competitor = db.query(Competitor).filter(Competitor.id == competitor_id).first()
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")

    db.delete(competitor)
    db.commit()
    return {"status": "deleted"}
