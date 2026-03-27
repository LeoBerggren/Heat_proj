from pydantic import BaseModel

#Score structure
class ScoreCreate(BaseModel):
    heat_id: int
    competitor_id: int
    judge_id: int
    value: float

#Competitors    
class CompetitorBase(BaseModel):
    name: str
    country: str | None = None
    
class CompetitorCreate(CompetitorBase):
    pass

class CompetitorRead(CompetitorBase):
    id: int

    class Config:
        orm_mode = True

#Judges
class JudgeBase(BaseModel):
    name: str
    country: str | None = None
    
class JudgeCreate(JudgeBase):
    pass

class JudgeRead(JudgeBase):
    id: int

    class Config:
        orm_mode = True
