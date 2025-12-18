from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.services.profiling import ProfilingService
from app.models.user import User

router = APIRouter()

@router.post("/refresh", status_code=200)
async def refresh_profiles(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger manual profiling run.
    """
    service = ProfilingService(db)
    await service.update_profiles(current_user.org_id if current_user.org_id else 1)
    return {"message": "Profiling started"}

@router.get("/", status_code=200)
async def get_profiles(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all attacker personas.
    """
    service = ProfilingService(db)
    personas = await service.get_personas(current_user.org_id if current_user.org_id else 1)
    return personas
