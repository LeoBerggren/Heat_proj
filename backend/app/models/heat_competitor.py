from sqlalchemy import Column, Integer, ForeignKey
from app.db import Base

class HeatCompetitor(Base):
    __tablename__ = "heat_competitors"

    id = Column(Integer, primary_key=True, index=True)
    heat_id = Column(Integer, ForeignKey("heats.id"))
    competitor_id = Column(Integer, ForeignKey("competitors.id"))
