from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.score import Score
from app.api.schemas import ScoreCreate

router = APIRouter()

@router.post("/scores")
def submit_score(score: ScoreCreate, db: Session = Depends(get_db)):
    db_score = Score(
        heat_id=score.heat_id,
        competitor_id=score.competitor_id,
        judge_id=score.judge_id,
        value=score.value
    )
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return {"status": "ok", "score_id": db_score.id}
