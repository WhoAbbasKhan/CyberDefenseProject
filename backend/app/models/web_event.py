from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from datetime import datetime
from app.db.session import Base

class WebEvent(Base):
    __tablename__ = "web_events"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    
    source_ip = Column(String, index=True)
    target_url = Column(String)
    method = Column(String) # GET, POST
    user_agent = Column(String, nullable=True)
    
    attack_type = Column(String) # sql_injection, xss, brute_force, bot
    severity = Column(String)
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Geo Data (Phase 4 placeholder)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
