from sqlalchemy import Column, Integer, String, DateTime, Enum, Float
from sqlalchemy.sql import func
from app.db.session import Base

class ThreatIndicator(Base):
    __tablename__ = "threat_indicators"

    id = Column(Integer, primary_key=True, index=True)
    
    indicator_value = Column(String, unique=True, index=True, nullable=False) # The IP, Domain, etc.
    indicator_type = Column(String, nullable=False) # IP, DOMAIN, FILE_HASH
    
    source = Column(String, default="System") # Name of the feed/source
    confidence = Column(Float, default=50.0) # 0-100
    
    description = Column(String, nullable=True) # e.g. "Known scanner"
    
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
