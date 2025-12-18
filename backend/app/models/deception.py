from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class DeceptionAsset(Base):
    __tablename__ = "deception_assets"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, index=True, nullable=False)
    
    asset_type = Column(String, nullable=False) # HONEYPOT_URL, CANARY_TOKEN, FAKE_USER
    token = Column(String, unique=True, index=True, nullable=False)
    label = Column(String, nullable=True) # e.g. "Fake Admin Login"
    
    configuration = Column(JSON, default={}) # Stores deployment details
    
    triggered_count = Column(Integer, default=0)
    last_triggered_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
