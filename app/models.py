from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from app.base import Base  # Import depuis base.py

class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    results = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
