from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class UserDevice(Base):
    __tablename__ = "user_devices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    fingerprint_hash = Column(String, index=True, nullable=False)
    device_name = Column(String, nullable=True) # e.g., "Chrome on Windows 10"
    
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    is_trusted = Column(Boolean, default=True)
    last_seen_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="devices")
