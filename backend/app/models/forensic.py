from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class ForensicEvidence(Base):
    __tablename__ = "forensic_evidence"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, index=True, nullable=False)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=True)
    
    evidence_type = Column(String, nullable=False) # LOG, SNAPSHOT, ARTIFACT
    data = Column(JSON, nullable=False) # The actual content
    
    # Immutability Fields
    cryptographic_hash = Column(String, nullable=False) # SHA256 of data + prev_hash
    previous_hash = Column(String, nullable=True) # Link to previous record in chain
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    incident = relationship("Incident")
