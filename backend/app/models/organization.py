from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.db.session import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    subscription_plan = Column(String, default="trial") # trial, starter, pro, enterprise
    
    trial_start = Column(DateTime, default=datetime.utcnow)
    trial_end = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=14))
    is_trial_active = Column(Boolean, default=True)
    
    users = relationship("User", back_populates="organization")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    behavioral_profiles = relationship("BehavioralProfile", back_populates="organization")
    anomalies = relationship("AnomalyEvent", back_populates="organization")
    incidents = relationship("Incident", back_populates="organization")
