from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from datetime import datetime
from app.db.session import Base

class LoginEvent(Base):
    __tablename__ = "login_events"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # If known user
    
    username_attempted = Column(String)
    source_ip = Column(String, index=True)
    success = Column(Boolean)
    
    attack_type = Column(String, nullable=True) # credential_stuffing, brute_force
    severity = Column(String, default="low")

    timestamp = Column(DateTime, default=datetime.utcnow)
    
    country = Column(String, nullable=True)
