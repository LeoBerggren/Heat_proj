from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.judge import Judge
from app.api.schemas import JudgeCreate, JudgeRead

router = APIRouter()

# CREATE
@router.post("/judges", response_model=JudgeRead)
def create_judge(data: JudgeCreate, db: Session = Depends(get_db)):
    judge = Judge(name=data.name, country=data.country)
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
    judge.country = data.country

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
