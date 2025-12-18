from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from datetime import datetime
from app.db.session import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Null if system action
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    
    action = Column(String, nullable=False, index=True) # e.g., "LOGIN", "CREATE_ORG"
    target = Column(String, nullable=True) # e.g., "User: 5"
    metadata_ = Column(JSON, nullable=True) # Renamed to avoid reserved word conflict if any, stored as 'metadata_'
    
    timestamp = Column(DateTime, default=datetime.utcnow)
