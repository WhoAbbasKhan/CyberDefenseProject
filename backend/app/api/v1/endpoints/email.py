from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.api.v1.deps_subscription import check_subscription_active, require_feature
from app.models.user import User
from app.models.email_event import EmailEvent
from app.services.email_detection import email_detector
from app.db.session import get_db

router = APIRouter()

class EmailIngest(BaseModel):
    sender: str
    recipient: EmailStr
    subject: str
    body: str
    links: List[str] = []

@router.post("/ingest", status_code=201)
async def ingest_email(
    email_data: EmailIngest,
    db: AsyncSession = Depends(get_db),
    org = Depends(check_subscription_active)
    # Note: In real world, this endpoint might be called by a gateway with an API Key, 
    # not necessarily a user session. For Phase 0, we assume it's an authenticated integration.
    # We might need a separate API Key auth schema later.
) -> Any:
    """
    Ingest and analyze an email.
    """
    # 1. Detect
    attack_type, confidence, severity = email_detector.analyze_email(
        sender=email_data.sender,
        subject=email_data.subject,
        body=email_data.body,
        links=email_data.links
    )
    
    # 2. Store if malicious (or even if clean, depending on policy. storing only attacks for now)
    if attack_type:
        event = EmailEvent(
            organization_id=org.id,
            sender_email=email_data.sender,
            recipient_email=email_data.recipient,
            subject=email_data.subject,
            body_snippet=email_data.body[:200],
            attack_type=attack_type,
            confidence_score=confidence,
            severity=severity
        )
        db.add(event)
        await db.commit()
        return {"status": "detected", "type": attack_type, "severity": severity}
    
    return {"status": "clean"}
