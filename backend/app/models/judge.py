from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Judge(Base):
    __tablename__ = "judges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    # relationship to judge sessions
    heats = relationship("JudgeHeat", back_populates="judge")

class JudgeHeat(Base):
    __tablename__ = "judge_heats"

    id = Column(Integer, primary_key=True)
    judge_id = Column(Integer, ForeignKey("judges.id"))
    heat_id = Column(Integer, ForeignKey("heats.id"))

    judge = relationship("Judge", back_populates="heats")

