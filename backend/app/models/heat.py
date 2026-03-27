from sqlalchemy import Column, Integer, String
from app.db import Base

class Heat(Base):
    __tablename__ = "heats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
