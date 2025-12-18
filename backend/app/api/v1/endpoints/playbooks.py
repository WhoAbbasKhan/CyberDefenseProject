from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.deps import get_db, get_current_user
from app.models.playbook import Playbook, PlaybookExecution
from app.models.user import User
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class PlaybookCreate(BaseModel):
    name: str
    trigger_type: str = "INCIDENT_CREATED"
    trigger_condition: dict
    actions: List[str]

@router.post("/", status_code=201)
async def create_playbook(
    pb_in: PlaybookCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new automation playbook.
    """
    playbook = Playbook(
        org_id=current_user.org_id if current_user.org_id else 1,
        name=pb_in.name,
        trigger_type=pb_in.trigger_type,
        trigger_condition=pb_in.trigger_condition,
        actions=pb_in.actions,
        is_active=True
    )
    db.add(playbook)
    await db.commit()
    await db.refresh(playbook)
    return playbook

@router.get("/", status_code=200)
async def get_playbooks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Playbook).where(Playbook.org_id == current_user.org_id))
    return result.scalars().all()

@router.get("/history", status_code=200)
async def get_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Join logic needed properly, but simple query for now
    # Check executions for owned playbooks
    # Simplified: Warning - this might be slow if many executions
    # Better: Filter by playbook.org_id join
    result = await db.execute(
        select(PlaybookExecution)
        .join(Playbook)
        .where(Playbook.org_id == current_user.org_id)
        .order_by(PlaybookExecution.created_at.desc())
    )
    return result.scalars().all()
