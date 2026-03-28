from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.competitor import Competitor
from app.api.schemas import CompetitorCreate, CompetitorRead

router = APIRouter(prefix="/admin/competitors", tags=["Admin Competitors"])


@router.get("/", response_model=list[CompetitorRead])
def list_competitors(db: Session = Depends(get_db)):
    return db.query(Competitor).all()


@router.post("/", response_model=CompetitorRead)
def create_competitor(data: CompetitorCreate, db: Session = Depends(get_db)):
    competitor = Competitor(name=data.name)
    db.add(competitor)
    db.commit()
    db.refresh(competitor)
    return competitor


@router.delete("/{competitor_id}")
def delete_competitor(competitor_id: int, db: Session = Depends(get_db)):
    competitor = db.query(Competitor).filter(Competitor.id == competitor_id).first()
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")

    db.delete(competitor)
    db.commit()
    return {"message": "Competitor deleted"}
