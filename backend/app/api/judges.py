from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.judge import Judge, JudgeHeat
from app.api.schemas import JudgeCreate, JudgeRead, JudgeScoreCreate
from app.models.heat import Heat
from app.models.score import Score
from app.models.competitor import Competitor

router = APIRouter(prefix="/judge", tags=["Judges"])


#JUDGE HEAT SELECTION
@router.post("/volunteer/{judge_id}/heat/{heat_id}")
def volunteer_for_heat(judge_id: int, heat_id: int, db: Session = Depends(get_db)):
    judge = db.query(Judge).filter(Judge.id == judge_id).first()
    if not judge:
        raise HTTPException(status_code=404, detail="Judge not found")

    heat = db.query(Heat).filter(Heat.id == heat_id).first()
    if not heat:
        raise HTTPException(status_code=404, detail="Heat not found")

    existing = (
        db.query(JudgeHeat)
        .filter(JudgeHeat.judge_id == judge_id, JudgeHeat.heat_id == heat_id)
        .first()
    )
    if existing:
        return {"message": "Already volunteering for this heat"}

    jh = JudgeHeat(judge_id=judge_id, heat_id=heat_id)
    db.add(jh)
    db.commit()

    return {"message": "Judge assigned to heat"}

###################

#JUDGE SCORE
@router.post("/score")
def submit_score(data: JudgeScoreCreate, db: Session = Depends(get_db)):
    # validate judge
    judge = db.query(Judge).filter(Judge.id == data.judge_id).first()
    if not judge:
        raise HTTPException(status_code=404, detail="Judge not found")

    # validate heat
    heat = db.query(Heat).filter(Heat.id == data.heat_id).first()
    if not heat:
        raise HTTPException(status_code=404, detail="Heat not found")

    # validate competitor
    competitor = db.query(Competitor).filter(Competitor.id == data.competitor_id).first()
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")

    # optional: validate judge is volunteering for this heat
    jh = (
        db.query(JudgeHeat)
        .filter(JudgeHeat.judge_id == data.judge_id,
                JudgeHeat.heat_id == data.heat_id)
        .first()
    )
    if not jh:
        raise HTTPException(status_code=403, detail="Judge not assigned to this heat")

    # optional: validate score range
    if not (0.0 <= data.score <= 10.0):
        raise HTTPException(status_code=400, detail="Score must be between 0 and 10")

    score = Score(
        judge_id=data.judge_id,
        heat_id=data.heat_id,
        competitor_id=data.competitor_id,
        wave=data.wave,
        score=data.score,
    )
    db.add(score)
    db.commit()
    db.refresh(score)

    return {"message": "Score submitted", "id": score.id}

###########
# CREATE
@router.post("/judges", response_model=JudgeRead)
def create_judge(data: JudgeCreate, db: Session = Depends(get_db)):
    judge = Judge(name=data.name)
    db.add(judge)
    db.commit()
    db.refresh(judge)
    return judge

# READ ALL
@router.get("/judges", response_model=list[JudgeRead])
def list_judges(db: Session = Depends(get_db)):
    return db.query(Judge).all()

# READ ONE
@router.get("/judges/{judge_id}", response_model=JudgeRead)
def get_judge(judge_id: int, db: Session = Depends(get_db)):
    judge = db.query(Judge).filter(Judge.id == judge_id).first()
    if not judge:
        raise HTTPException(status_code=404, detail="judge not found")
    return judge

# UPDATE
@router.put("/judges/{judge_id}", response_model=JudgeRead)
def update_judge(judge_id: int, data: JudgeCreate, db: Session = Depends(get_db)):
    judge = db.query(Judge).filter(Judge.id == judge_id).first()
    if not judge:
        raise HTTPException(status_code=404, detail="Judge not found")

    judge.name = data.name

    db.commit()
    db.refresh(judge)
    return judge

# DELETE
@router.delete("/judges/{judge_id}")
def delete_judge(judge_id: int, db: Session = Depends(get_db)):
    judge = db.query(Judge).filter(Judge.id == judge_id).first()
    if not judge:
        raise HTTPException(status_code=404, detail="Judge not found")

    db.delete(judge)
    db.commit()
    return {"status": "deleted"}
