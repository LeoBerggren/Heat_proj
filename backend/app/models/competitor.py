from sqlalchemy import Column, Integer, String
from app.db import Base

class Competitor(Base):
    __tablename__ = "competitors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    country = Column(String, nullable=True)
