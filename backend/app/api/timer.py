from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.db import get_db
from app.models.heat import Heat

router = APIRouter(prefix="/heat", tags=["Heat Timer"])

@router.get("/{heat_id}/timer")
def get_heat_timer(heat_id: int, db: Session = Depends(get_db)):
    heat = db.query(Heat).filter(Heat.id == heat_id).first()
    if not heat:
        raise HTTPException(status_code=404, detail="Heat not found")

    # Heat not started
    if not heat.start_time:
        return {
            "heat_id": heat_id,
            "is_running": False,
            "time_remaining": None,
            "duration": heat.duration_minutes * 60,
            "start_time": heat.start_time,
            "end_time": heat.end_time
        }

    now = datetime.utcnow()
    end = heat.end_time
    remaining = int((end - now).total_seconds())

    if remaining <= 0:
        heat.status = "finished"
        db.commit()
        return {
            "heat_id": heat_id,
            "is_running": False,
            "time_remaining": 0,
            "duration": heat.duration_minutes * 60,
            "start_time": heat.start_time,
            "end_time": heat.end_time
        }
    
    return {
        "heat_id": heat_id,
        "is_running": remaining > 0,
        "time_remaining": max(0, remaining),
        "duration": heat.duration_minutes * 60,
        "start_time": heat.start_time,
        "end_time": heat.end_time
    }

    
