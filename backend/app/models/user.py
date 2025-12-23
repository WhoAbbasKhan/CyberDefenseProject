from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    google_sub = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="employee") # super_admin, org_admin, security, employee
    
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    organization = relationship("Organization", back_populates="users")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    devices = relationship("UserDevice", back_populates="user")
    auth_providers = relationship("AuthProvider", back_populates="user")
