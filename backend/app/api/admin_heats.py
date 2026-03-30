from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.heat import Heat
from app.api.schemas import HeatCreate, HeatRead
from app.models.score import Score
from app.models.judge import Judge
from app.api.schemas import JudgeBreakdownResponse, JudgeBreakdownEntry, JudgeScoreEntry

router = APIRouter(prefix="/admin/heats", tags=["Admin Heats"])


admin_judge_router = APIRouter(prefix="/admin/heats", tags=["Admin Judge Breakdown"])


#JUDGE BREAKDOWN ADMIN
@admin_judge_router.get("/{heat_id}/judge_breakdown", response_model=JudgeBreakdownResponse)
def judge_breakdown(heat_id: int, db: Session = Depends(get_db)):
    heat = db.query(Heat).filter(Heat.id == heat_id).first()
    if not heat:
        raise HTTPException(status_code=404, detail="Heat not found")

    scores = db.query(Score).filter(Score.heat_id == heat_id).all()
    if not scores:
        return JudgeBreakdownResponse(heat_id=heat_id, judges=[])

    # group by judge
    by_judge: dict[int, list[Score]] = {}
    for s in scores:
        by_judge.setdefault(s.judge_id, []).append(s)

    judges_data: list[JudgeBreakdownEntry] = []

    for judge_id, judge_scores in by_judge.items():
        judge = db.query(Judge).filter(Judge.id == judge_id).first()
        entries = [
            JudgeScoreEntry(
                competitor_id=s.competitor_id,
                wave=s.wave,
                score=s.score
            )
            for s in judge_scores
        ]
        judges_data.append(
            JudgeBreakdownEntry(
                judge_id=judge_id,
                name=judge.name if judge else None,
                scores=entries
            )
        )

    return JudgeBreakdownResponse(
        heat_id=heat_id,
        judges=judges_data
    )


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
