from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.websocket_manager import manager

from app.db import get_db
from app.models.score import Score
from app.api.schemas import ScoreCreate
from app.api.schemas import ScoreRead

router = APIRouter()

#CREATE/SUBMIT SCORE
@router.post("/scores", response_model=ScoreRead)
async def submit_score(data: ScoreCreate, db: Session = Depends(get_db)):
    db_score = Score(
        heat_id=data.heat_id,
        competitor_id=data.competitor_id,
        judge_id=data.judge_id,
        value=data.value
    )
    db.add(db_score)
    db.commit()
    db.refresh(db_score)

    # Broadcast using the DB object, not the Pydantic input
    await manager.broadcast({
        "type": "new_score",
        "score": {
            "id": db_score.id,
            "heat_id": db_score.heat_id,
            "competitor_id": db_score.competitor_id,
            "judge_id": db_score.judge_id,
            "value": db_score.value,
            "timestamp": db_score.timestamp.isoformat()
        }
    })

    return db_score

# READ ALL
@router.get("/scores", response_model=list[ScoreRead])
def list_scores(db: Session = Depends(get_db)):
    return db.query(Score).all()

# READ ONE
@router.get("/scores/{score_id}", response_model=ScoreRead)
def get_score(score_id: int, db: Session = Depends(get_db)):
    score = db.query(Score).filter(Score.id == score_id).first()
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")
    return score

# READ BY HEAT
@router.get("/heats/{heat_id}/scores", response_model=list[ScoreRead])
def get_scores_for_heat(heat_id: int, db: Session = Depends(get_db)):
    return db.query(Score).filter(Score.heat_id == heat_id).all()

# READ BY COMPETITOR
@router.get("/competitors/{competitor_id}/scores", response_model=list[ScoreRead])
def get_scores_for_competitor(competitor_id: int, db: Session = Depends(get_db)):
    return db.query(Score).filter(Score.competitor_id == competitor_id).all()

# DELETE
@router.delete("/scores/{score_id}")
def delete_score(score_id: int, db: Session = Depends(get_db)):
    score = db.query(Score).filter(Score.id == score_id).first()
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")

    db.delete(score)
    db.commit()
    return {"status": "deleted"}
