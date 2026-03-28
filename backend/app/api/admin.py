from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.heat import Heat
from app.websocket_manager import manager

router = APIRouter()

@router.post("/heats/{heat_id}/start")
async def start_heat(heat_id: int, db: Session = Depends(get_db)):
    heat = db.query(Heat).filter(Heat.id == heat_id).first()
    if not heat:
        raise HTTPException(status_code=404, detail="Heat not found")

    heat.status = "running"
    db.commit()

    # Broadcast to spectators
    await manager.broadcast({
        "type": "heat_status",
        "heat_id": heat_id,
        "status": "running"
    })

    return {"message": "Heat started", "heat_id": heat_id}

@router.post("/heats/{heat_id}/finish")
async def finish_heat(heat_id: int, db: Session = Depends(get_db)):
    heat = db.query(Heat).filter(Heat.id == heat_id).first()
    if not heat:
        raise HTTPException(status_code=404, detail="Heat not found")

    heat.status = "finished"
    db.commit()

    # Broadcast to spectators
    await manager.broadcast({
        "type": "heat_status",
        "heat_id": heat_id,
        "status": "finished"
    })

    # Also trigger leaderboard update
    await manager.broadcast({
        "type": "leaderboard_update",
        "heat_id": heat_id
    })

    return {"message": "Heat finished", "heat_id": heat_id}

@router.post("/admin/broadcast/leaderboard/{heat_id}")
async def broadcast_leaderboard(heat_id: int):
    await manager.broadcast({
        "type": "leaderboard_update",
        "heat_id": heat_id
    })
    return {"message": "Leaderboard update broadcast", "heat_id": heat_id}
