from sqlalchemy import Column, Integer, String
from app.db import Base

class Judge(Base):
    __tablename__ = "judges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
