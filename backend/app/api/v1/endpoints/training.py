from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel

from app.api import deps
from app.db.session import get_db
from app.models.user import User
from app.models.training import TrainingModule, UserTraining, TrainingStatus

router = APIRouter()

# --- Schemas ---
class TrainingModuleBase(BaseModel):
    title: str
    description: str
    category: str
    duration_minutes: int
    content: Optional[str] = None

class TrainingModuleCreate(TrainingModuleBase):
    pass

class TrainingModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    duration_minutes: Optional[int] = None
    content: Optional[str] = None

class TrainingModuleSchema(TrainingModuleBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserTrainingSchema(BaseModel):
    id: int
    module: TrainingModuleSchema
    status: str
    assigned_at: datetime
    due_date: Optional[datetime]
    score: Optional[int]

class AssignRequest(BaseModel):
    user_id: int
    module_id: int

class TriggerRequest(BaseModel):
    email: str
    trigger_type: str # e.g., "phishing_click", "weak_password"

# --- Endpoints ---

# 1. CRUD for Modules (Admin Only)

@router.get("/", response_model=List[TrainingModuleSchema])
async def list_modules(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """
    List all available training modules.
    """
    result = await db.execute(select(TrainingModule).offset(skip).limit(limit))
    return result.scalars().all()

@router.post("/", response_model=TrainingModuleSchema)
async def create_module(
    module_in: TrainingModuleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
):
    """
    Create a new training module (Admin only).
    """
    module = TrainingModule(**module_in.dict())
    db.add(module)
    await db.commit()
    await db.refresh(module)
    return module

@router.put("/{module_id}", response_model=TrainingModuleSchema)
async def update_module(
    module_id: int,
    module_in: TrainingModuleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
):
    """
    Update a training module (Admin only).
    """
    result = await db.execute(select(TrainingModule).where(TrainingModule.id == module_id))
    module = result.scalars().first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
        
    update_data = module_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(module, field, value)
        
    db.add(module)
    await db.commit()
    await db.refresh(module)
    return module

@router.delete("/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_module(
    module_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
):
    """
    Delete a training module (Admin only).
    """
    result = await db.execute(select(TrainingModule).where(TrainingModule.id == module_id))
    module = result.scalars().first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
        
    await db.delete(module)
    await db.commit()
    return None

# 2. User User Progress

@router.get("/me", response_model=List[UserTrainingSchema])
async def get_my_training(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Fetch user trainings with module relation
    result = await db.execute(
        select(UserTraining)
        .where(UserTraining.user_id == current_user.id)
        .options(joinedload(UserTraining.module)) # Eager load
    )
    trainings = result.scalars().all()
    
    # Map to schema (simplified)
    return [
        UserTrainingSchema(
            id=t.id,
            status=t.status,
            assigned_at=t.assigned_at,
            due_date=t.due_date,
            score=t.score,
            module=TrainingModuleSchema.from_orm(t.module)
        ) for t in trainings
    ]

@router.post("/trigger")
async def trigger_training(
    trigger: TriggerRequest,
    db: AsyncSession = Depends(get_db),
    # In real app, this might be called by internal services, so we might check for Service Token or Admin
    current_user: User = Depends(deps.get_current_active_superuser) 
):
    # 1. Find User
    result = await db.execute(select(User).where(User.email == trigger.email))
    target_user = result.scalars().first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Determine Module based on Trigger
    # Mock Logic: If trigger is "phishing_click", assign "Phishing 101"
    # We need to make sure the module exists. For this mock, we'll create it if missing.
    
    module_title = "General Security"
    if trigger.trigger_type == "phishing_click":
        module_title = "Phishing Awareness 101"
    elif trigger.trigger_type == "weak_password":
        module_title = "Password Security Basics"
        
    # Check if module exists
    res_mod = await db.execute(select(TrainingModule).where(TrainingModule.title == module_title))
    module = res_mod.scalars().first()
    
    if not module:
        # Auto-create for demo
        module = TrainingModule(
            title=module_title,
            description=f"Auto-generated training for {trigger.trigger_type}",
            category="security",
            content="## Important Security Training\n\nPlease read this carefully...",
            duration_minutes=15
        )
        db.add(module)
        await db.flush()
        
    # 3. Assign to User (if not already assigned/in-progress)
    # Check existing
    res_exist = await db.execute(
        select(UserTraining).where(
            UserTraining.user_id == target_user.id,
            UserTraining.module_id == module.id,
            UserTraining.status.in_([TrainingStatus.ASSIGNED, TrainingStatus.IN_PROGRESS])
        )
    )
    existing = res_exist.scalars().first()
    
    if existing:
        return {"message": "Training already assigned", "training_id": existing.id}
        
    new_training = UserTraining(
        user_id=target_user.id,
        module_id=module.id,
        organization_id=target_user.organization_id,
        status=TrainingStatus.ASSIGNED,
        due_date=datetime.utcnow() + timedelta(days=7)
    )
    db.add(new_training)
    await db.commit()
    
    return {"message": "Training assigned via trigger", "module": module.title, "user": target_user.email}

@router.post("/complete/{training_id}")
async def complete_training(
    training_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    result = await db.execute(select(UserTraining).where(UserTraining.id == training_id, UserTraining.user_id == current_user.id))
    training = result.scalars().first()
    
    if not training:
        raise HTTPException(status_code=404, detail="Training not found")
        
    training.status = TrainingStatus.COMPLETED
    training.completed_at = datetime.utcnow()
    training.score = 100 # Mock score
    
    await db.commit()
    return {"status": "completed"}
