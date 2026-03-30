from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from datetime import datetime
from app.db import Base

class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True)
    heat_id = Column(Integer, ForeignKey("heats.id"))
    competitor_id = Column(Integer)
    judge_id = Column(Integer,  ForeignKey("judges.id"))
    wave = Column(Integer)  # wave number
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)