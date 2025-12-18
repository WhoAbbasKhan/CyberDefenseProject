from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class AttackerPersona(Base):
    __tablename__ = "attacker_personas"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, index=True, nullable=False)
    
    name = Column(String, nullable=False) # e.g. "Cluster-12A" or "Lazarus"
    sophistication = Column(String, default="UNKNOWN") # SCRIPT_KIDDIE, APT, BOTNET
    
    related_ips = Column(JSON, default=[]) # List of IPs linked to this persona
    related_incidents = Column(JSON, default=[]) # List of Incident IDs
    
    campaign_status = Column(String, default="ACTIVE") # ACTIVE, DORMANT
    
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    description = Column(String, nullable=True)
