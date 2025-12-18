from typing import Any
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.api.v1.deps_subscription import check_subscription_active
from app.core.websockets import manager
from app.models.web_event import WebEvent
from app.models.login_event import LoginEvent
from app.services.web_detection import web_detector
from app.db.session import get_db
from pydantic import BaseModel

router = APIRouter()

class WebLog(BaseModel):
    url: str
    method: str
    user_agent: str
    payload: str = ""
    ip: str

class LoginLog(BaseModel):
    username: str
    success: bool
    ip: str

@router.post("/log/web", status_code=201)
async def log_web_event(
    event_in: WebLog,
    db: AsyncSession = Depends(get_db),
    org = Depends(check_subscription_active)
):
    attack_type, severity = web_detector.detect_web_attack(
        event_in.method, event_in.url, event_in.user_agent, event_in.payload
    )
    
    if attack_type: # Only log attacks? Roadmap says "Watch everything... It constantly monitors".
        # We should log everything but maybe only ALERT on attacks.
        # Roadmap says "Logs it instantly".
        # For data volume in Phase 0, let's log everything but highlight attacks.
        pass

    event = WebEvent(
        organization_id=org.id,
        source_ip=event_in.ip,
        target_url=event_in.url,
        method=event_in.method,
        user_agent=event_in.user_agent,
        attack_type=attack_type,
        severity=severity
    )
    db.add(event)
    await db.commit()
    
    if attack_type:
        await manager.broadcast({
            "type": "web_attack",
            "attack_type": attack_type, 
            "severity": severity,
            "ip": event_in.ip
        }, org.id)
        
    return {"status": "logged", "attack": attack_type}

@router.get("/events")
async def get_web_events(
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    org = Depends(check_subscription_active)
):
    """
    List recent web events/attacks.
    """
    from sqlalchemy.future import select
    res = await db.execute(
        select(WebEvent)
        .where(WebEvent.organization_id == org.id)
        .order_by(WebEvent.timestamp.desc())
        .limit(limit)
    )
    events = res.scalars().all()
    return events

@router.post("/log/login", status_code=201)
async def log_login_event(
    event_in: LoginLog,
    db: AsyncSession = Depends(get_db),
    org = Depends(check_subscription_active)
):
    # Detect
    # (Simple logic: if we had redis, we'd incr key)
    
    event = LoginEvent(
        organization_id=org.id,
        username_attempted=event_in.username,
        source_ip=event_in.ip,
        success=event_in.success,
        attack_type=None, # Filled by detector if real logic exists
        severity="low"
    )
    db.add(event)
    await db.commit()
    
    if not event_in.success:
        # Simulate alerting for failed login
        await manager.broadcast({
            "type": "login_failed",
            "username": event_in.username,
            "ip": event_in.ip
        }, org.id)

    return {"status": "logged"}

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str, # passed as query param ?token=...
    db: AsyncSession = Depends(get_db) 
):
    # Validate Token
    from app.core import security
    from jose import jwt
    from app.core.config import settings
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
    except:
        await websocket.close(code=1008)
        return

    # Get User Org
    from sqlalchemy import select
    from app.models.user import User
    
    # We need a new session as Depends doesn't work well in WS directly in some versions?
    # Actually Depends works in FastAPI WS.
    
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalars().first()
    
    if not user:
        await websocket.close()
        return

    await manager.connect(websocket, user.organization_id)
    try:
        while True:
            await websocket.receive_text() # Keep alive
    except WebSocketDisconnect:
        manager.disconnect(websocket, user.organization_id)
