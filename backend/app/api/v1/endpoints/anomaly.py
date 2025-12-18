from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.services.anomaly import AnomalyService
from app.models.user import User
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class AnalyzeRequest(BaseModel):
    user_id: int
    ip_address: str
    timestamp: datetime = None

@router.post("/analyze/login", status_code=200)
async def analyze_login(
    request: AnalyzeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Manual trigger to analyze a login event.
    In production, this would be called by the Auth service automatically.
    """
    if current_user.role not in ["super_admin", "admin", "it_security"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    service = AnomalyService(db)
    
    # Use current time if not provided
    ts = request.timestamp or datetime.utcnow()
    
    # 1. Detect
    result = await service.detect_login_anomaly(
        org_id=current_user.org_id,
        user_id=request.user_id,
        login_time=ts,
        ip_address=request.ip_address
    )
    
    # 2. Update Baseline (Async mostly, but for now sync to ensure data flow)
    await service.update_login_baseline(
        org_id=current_user.org_id,
        user_id=request.user_id,
        login_time=ts,
        ip_address=request.ip_address
    )
    
    return result

@router.post("/train/simulate", status_code=200)
async def simulate_training_data(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Seed baseline data for the current user to enable ML detection.
    Adds 30 logins at 9:00 AM.
    """
    service = AnomalyService(db)
    base_time = datetime.utcnow().replace(hour=9, minute=0)
    
    for i in range(30):
        # Vary slightly
        ts = base_time.replace(minute=i % 60)
        await service.update_login_baseline(
            org_id=current_user.org_id,
            user_id=current_user.id,
            login_time=ts,
            ip_address="127.0.0.1"
        )
        
    return {"message": "Simulated 30 normal logins for baseline."}
