from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.services.threat import ThreatIntelService
from app.models.user import User
from pydantic import BaseModel

router = APIRouter()

class IngestRequest(BaseModel):
    source: str
    indicators: list[dict] # [ {value, type, desc} ]

@router.post("/ingest", status_code=200)
async def ingest_feed(
    request: IngestRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Manually ingest threat intel.
    """
    if current_user.role not in ["super_admin", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    service = ThreatIntelService(db)
    await service.ingest_feed(request.source, request.indicators)
    return {"message": f"Ingested {len(request.indicators)} indicators"}
