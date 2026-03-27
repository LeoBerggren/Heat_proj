from pydantic import BaseModel

class ScoreCreate(BaseModel):
    heat_id: int
    competitor_id: int
    judge_id: int
    value: float
class CompetitorBase(BaseModel):
    name: str
    country: str | None = None
    
class CompetitorCreate(CompetitorBase):
    pass

class CompetitorRead(CompetitorBase):
    id: int

    class Config:
        orm_mode = True
