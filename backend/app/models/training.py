from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.session import Base

class TrainingStatus(str, enum.Enum):
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"

class TrainingModule(Base):
    __tablename__ = "training_modules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    content = Column(Text) # Markdown content or URL to video
    duration_minutes = Column(Integer, default=15)
    
    # "phishing", "password_security", "social_engineering"
    category = Column(String, index=True) 
    
    created_at = Column(DateTime, default=datetime.utcnow)

class UserTraining(Base):
    __tablename__ = "user_trainings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    module_id = Column(Integer, ForeignKey("training_modules.id"))
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    
    status = Column(String, default=TrainingStatus.ASSIGNED)
    score = Column(Integer, nullable=True) # 0-100 if quiz
    
    assigned_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)

    user = relationship("User", backref="trainings")
    module = relationship("TrainingModule")
