# app/models/settings.py

from sqlalchemy import Column, Integer, String
from app.db import Base

class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(String)
