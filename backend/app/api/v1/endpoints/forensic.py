from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.services.forensic import ForensicService
from app.models.user import User
from pydantic import BaseModel

router = APIRouter()

class EvidenceLog(BaseModel):
    type: str # LOG, FILE_HASH
    data: dict
    incident_id: int = None

@router.post("/log", status_code=201)
async def log_evidence_api(
    ev_in: EvidenceLog,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Manually log evidence.
    """
    service = ForensicService(db)
    evidence = await service.log_evidence(
        org_id=current_user.org_id if current_user.org_id else 1,
        evidence_type=ev_in.type,
        data=ev_in.data,
        incident_id=ev_in.incident_id
    )
    return {"id": evidence.id, "hash": evidence.cryptographic_hash}

@router.get("/verify", status_code=200)
async def verify_integrity(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Verify chain of custody.
    """
    service = ForensicService(db)
    return await service.verify_chain(current_user.org_id if current_user.org_id else 1)

@router.get("/timeline/{incident_id}", status_code=200)
async def get_incident_timeline(
    incident_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ForensicService(db)
    return await service.get_timeline(incident_id)
