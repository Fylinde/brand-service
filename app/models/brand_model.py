from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.database import BaseModel

class BrandModel(BaseModel):
    __tablename__ = 'brands'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(String(500), nullable=True)
    status = Column(Boolean, default=True)  # Indicates if the brand is active or deactivated
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)  # Soft deletion support
