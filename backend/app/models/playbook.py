from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Playbook(Base):
    __tablename__ = "playbooks"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, index=True, nullable=False)
    
    name = Column(String, nullable=False) # "Phishing Auto-Block"
    description = Column(String, nullable=True)
    
    # Trigger Logic
    trigger_type = Column(String, default="INCIDENT_CREATED") # INCIDENT_CREATED, INCIDENT_UPDATED
    trigger_condition = Column(JSON, default={}) # e.g. {"severity": "CRITICAL", "type": "Phishing"}
    
    # Actions
    actions = Column(JSON, default=[]) # List of actions: ["BLOCK_IP", "NOTIFY_ADMIN"]
    
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    executions = relationship("PlaybookExecution", back_populates="playbook")

class PlaybookExecution(Base):
    __tablename__ = "playbook_executions"

    id = Column(Integer, primary_key=True, index=True)
    playbook_id = Column(Integer, ForeignKey("playbooks.id"), nullable=False)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=True)
    
    status = Column(String, default="PENDING") # PENDING, SUCCESS, FAILED
    logs = Column(JSON, default=[])
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    playbook = relationship("Playbook", back_populates="executions")
