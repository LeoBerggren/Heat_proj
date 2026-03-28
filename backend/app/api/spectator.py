from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.heat import Heat
from app.models.heat_competitor import HeatCompetitor
from app.models.competitor import Competitor
from app.models.score import Score

router = APIRouter()

@router.get("/spectator/heat/{heat_id}")
def get_heat_spectator_view(heat_id: int, db: Session = Depends(get_db)):
    # 1. Get heat
    heat = db.query(Heat).filter(Heat.id == heat_id).first()
    if not heat:
        raise HTTPException(status_code=404, detail="Heat not found")

    # 2. Get competitors in this heat
    assignments = db.query(HeatCompetitor).filter(HeatCompetitor.heat_id == heat_id).all()
    competitor_ids = [a.competitor_id for a in assignments]

    competitors = db.query(Competitor).filter(Competitor.id.in_(competitor_ids)).all()

    # 3. Get scores for this heat
    scores = db.query(Score).filter(Score.heat_id == heat_id).all()

    # 4. Organize scores by competitor
    competitor_scores = {c.id: [] for c in competitors}
    for s in scores:
        competitor_scores[s.competitor_id].append(s.value)

    # 5. Calculate rankings
    leaderboard = []
    for c in competitors:
        waves = sorted(competitor_scores[c.id], reverse=True)
        best_two = waves[:2]
        total = sum(best_two)
        leaderboard.append({
            "competitor_id": c.id,
            "name": c.name,
            "waves": waves,
            "best_two": best_two,
            "total": total
        })

    leaderboard.sort(key=lambda x: x["total"], reverse=True)

    return {
        "heat": {
            "id": heat.id,
            "round": heat.round,
            "start_time": heat.start_time,
            "end_time": heat.end_time,
            "status": heat.status
        },
        "competitors": [
            {"id": c.id, "name": c.name}
            for c in competitors
        ],
        "leaderboard": leaderboard
    }
