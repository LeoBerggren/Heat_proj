# app/api/admin_settings.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.settings import Setting

router = APIRouter(prefix="/admin/settings", tags=["Admin Settings"])

@router.get("/judge_code")
def get_judge_code(db: Session = Depends(get_db)):
    setting = db.query(Setting).filter(Setting.key == "judge_code").first()
    if not setting:
        return {"value": None}
    return {"value": setting.value}

@router.put("/judge_code")
def set_judge_code(data: dict, db: Session = Depends(get_db)):
    setting = db.query(Setting).filter(Setting.key == "judge_code").first()
    setting.value = data["value"]
    db.commit()
    return {"message": "updated"}

