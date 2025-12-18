from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    status = Column(String, default="OPEN") # OPEN, INVESTIGATING, RESOLVED
    severity = Column(String, default="MEDIUM") # LOW, MEDIUM, HIGH, CRITICAL
    kill_chain_stage = Column(String, nullable=True) # RECON, DELIVERY, EXPLOITATION, ACTION
    
    summary = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    # Linked Entities
    actor_ip = Column(String, index=True, nullable=True)
    actor_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # References to raw events (could be specific tables, but JSON is flexible for correlation)
    linked_event_ids = Column(JSON, default=[]) 
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="incidents")
    user = relationship("User")
