from pydantic import BaseModel

class ScoreCreate(BaseModel):
    heat_id: int
    competitor_id: int
    judge_id: int
    value: float
