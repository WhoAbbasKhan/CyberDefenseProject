from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.session import Base

class DefenseRule(Base):
    __tablename__ = "defense_rules"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    
    name = Column(String)
    if_type = Column(String) # e.g. SQL Injection
    if_severity = Column(String) # e.g. Critical
    then_action = Column(String) # e.g. Block IP
    
    is_active = Column(Boolean, default=True)
