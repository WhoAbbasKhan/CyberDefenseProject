from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class AuthProvider(Base):
    __tablename__ = "auth_providers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider_type = Column(String, nullable=False)  # 'google', 'passkey'
    
    # For Passkeys (WebAuthn)
    credential_id = Column(String, unique=True, index=True, nullable=True)
    public_key = Column(LargeBinary, nullable=True)
    sign_count = Column(Integer, default=0)
    device_name = Column(String, nullable=True)
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="auth_providers")
