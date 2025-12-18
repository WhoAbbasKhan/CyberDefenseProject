from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.deps import get_db, get_current_user
from app.api.v1.deps_subscription import check_subscription_active
from app.models.defense_rule import DefenseRule
from app.services.defense import BlockedIP
from pydantic import BaseModel

router = APIRouter()

class DefenseRuleCreate(BaseModel):
    name: str
    if_type: str
    if_severity: str
    then_action: str
    is_active: bool = True

class DefenseRuleOut(DefenseRuleCreate):
    id: int

@router.get("/rules", response_model=list[DefenseRuleOut])
async def get_rules(
    db: AsyncSession = Depends(get_db),
    org = Depends(check_subscription_active)
):
    result = await db.execute(
        select(DefenseRule).where(DefenseRule.organization_id == org.id)
    )
    return result.scalars().all()

@router.post("/rules", response_model=DefenseRuleOut)
async def create_rule(
    rule_in: DefenseRuleCreate,
    db: AsyncSession = Depends(get_db),
    org = Depends(check_subscription_active)
):
    rule = DefenseRule(
        organization_id=org.id,
        name=rule_in.name,
        if_type=rule_in.if_type,
        if_severity=rule_in.if_severity,
        then_action=rule_in.then_action,
        is_active=rule_in.is_active
    )
    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return rule

@router.delete("/rules/{rule_id}")
async def delete_rule(
    rule_id: int,
    db: AsyncSession = Depends(get_db),
    org = Depends(check_subscription_active)
):
    result = await db.execute(
        select(DefenseRule).where(DefenseRule.id == rule_id, DefenseRule.organization_id == org.id)
    )
    rule = result.scalars().first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    await db.delete(rule)
    await db.commit()
    return {"status": "deleted"}

# Blocked IPs
@router.get("/blocked")
async def get_blocked_ips(
    db: AsyncSession = Depends(get_db),
    org = Depends(check_subscription_active)
):
    result = await db.execute(
        select(BlockedIP).where(BlockedIP.organization_id == org.id)
    )
    return result.scalars().all()
