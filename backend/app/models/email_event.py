from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base
import enum

class EmailSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class EmailEvent(Base):
    __tablename__ = "email_events"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    
    sender_email = Column(String)
    recipient_email = Column(String)
    subject = Column(String)
    body_snippet = Column(Text, nullable=True) # Don't store full body if sensitive
    
    attack_type = Column(String) # phishing, spoofing, etc.
    confidence_score = Column(Float)
    severity = Column(String) # low, medium, high, critical (stored as string or enum)
    
    detected_at = Column(DateTime, default=datetime.utcnow)
    
    # Metadata for analysis (headers, links found) - Stored as JSON usually, simplified here
    # meta_data = Column(JSON, nullable=True) 
