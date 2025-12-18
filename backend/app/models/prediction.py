from sqlalchemy import Column, Integer, String, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class AttackPrediction(Base):
    __tablename__ = "attack_predictions"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, index=True, nullable=False) # Simplified: No FK for decoupled MVP or add ForeignKey("organizations.id")
    
    predicted_attack_type = Column(String, nullable=False)
    target_asset = Column(String, nullable=True) # "User:123" or "Server:DB"
    
    probability = Column(Float, nullable=False) # 0-100
    time_horizon = Column(String, default="24h")
    
    status = Column(String, default="PENDING") # PENDING, REALIZED, DISMISSED
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Optional: Link to Organization if strict FK desired
    # organization = relationship("Organization")
