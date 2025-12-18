from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class BehavioralProfile(Base):
    __tablename__ = "behavioral_profiles"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    entity_type = Column(String, nullable=False)  # 'user' or 'ip'
    entity_id = Column(String, nullable=False)    # user_id or ip_address
    
    # JSON Blob for rolling baseline stats
    # Example: { "avg_login_time": 14.5, "req_frequency": 50, "last_10_logins": [...] }
    baseline_data = Column(JSON, default={})
    
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="behavioral_profiles")


class AnomalyEvent(Base):
    __tablename__ = "anomaly_events"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    event_type = Column(String, nullable=False)   # 'login_anomaly', 'usage_spike'
    severity_score = Column(Float, nullable=False) # 0.0 to 100.0
    confidence_score = Column(Float, nullable=False) # 0.0 to 1.0
    
    details = Column(JSON, default={}) # Reasoning: "Login at 3AM (avg 9AM)"
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="anomalies")
