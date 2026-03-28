from pydantic import BaseModel
from datetime import datetime


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
    
class JudgeCreate(JudgeBase):
    pass

class JudgeRead(JudgeBase):
    id: int

    class Config:
        orm_mode = True


# Events
class EventBase(BaseModel):
    name: str
    location: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None

class EventCreate(EventBase):
    pass

class EventRead(EventBase):
    id: int

    class Config:
        orm_mode = True

# Heats
class HeatBase(BaseModel):
    event_id: int
    round: str
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: str = "pending"

class HeatCreate(BaseModel):
    round: str
    start_time: datetime | None = None
    end_time: datetime | None = None
    event_id: int | None = None   # optional for now

class HeatRead(BaseModel):
    id: int
    event_id: int | None = None
    round: str
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: str

    class Config:
        orm_mode = True

# Heat–Competitor assignments
class HeatCompetitorBase(BaseModel):
    heat_id: int
    competitor_id: int

class HeatCompetitorCreate(HeatCompetitorBase):
    pass

class HeatCompetitorRead(HeatCompetitorBase):
    id: int

    class Config:
        orm_mode = True

# Scores
class ScoreBase(BaseModel):
    heat_id: int
    competitor_id: int
    judge_id: int
    value: float

class ScoreCreate(ScoreBase):
    pass

class ScoreRead(ScoreBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
