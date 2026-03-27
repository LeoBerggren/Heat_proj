from sqlalchemy import Column, Integer, String,  DateTime, ForeignKey
from app.db import Base

class Heat(Base):
    __tablename__ = "heats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    round = Column(String)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    status = Column(String, default="pending")
