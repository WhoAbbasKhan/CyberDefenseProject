from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.services.deception import DeceptionService
from app.models.user import User
from pydantic import BaseModel

router = APIRouter()

class AssetCreate(BaseModel):
    type: str # HONEYPOT_URL, CANARY_TOKEN
    label: str
    config: dict = {}

@router.post("/assets", status_code=201)
async def create_asset(
    asset_in: AssetCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new deception asset (Honeypot/Canary).
    """
    service = DeceptionService(db)
    asset = await service.create_asset(
        org_id=current_user.org_id if current_user.org_id else 1,
        asset_type=asset_in.type,
        label=asset_in.label,
        config=asset_in.config
    )
    return {"token": asset.token, "id": asset.id}

@router.get("/trap/{token}")
async def honey_pot_endpoint(
    token: str,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    The Trap Endpoint.
    ANY access here triggers a CRITICAL incident.
    """
    service = DeceptionService(db)
    ip = request.client.host if request.client else "0.0.0.0"
    
    await service.trigger_trap(token, {
        "ip_address": ip,
        "user_agent": request.headers.get("user-agent"),
        "headers": dict(request.headers)
    })
    
    # Return a dummy interesting response to keep them engaged?
    # Or just 404/403 to confuse them?
    # "Honey" response:
    return {"status": "error", "code": "DB_CONNECTION_FAIL", "debug_trace": "admin_user: root"} 
