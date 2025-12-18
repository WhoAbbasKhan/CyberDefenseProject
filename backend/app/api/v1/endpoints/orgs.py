from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api import deps
from app.models.user import User
from app.models.organization import Organization
from app.db.session import get_db

router = APIRouter()

@router.post("/invite", status_code=201)
async def invite_user(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    email: str,
    role: str = "employee"
) -> Any:
    """
    Invite a user to the organization.
    Only Admins can invite.
    """
    if current_user.role not in ["super_admin", "org_admin"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == email))
    if result.scalars().first():
         raise HTTPException(status_code=400, detail="User already exists")
         
    # Create simplified user (placeholder password, should send email in real app)
    # For Phase 0, we just create them with a default password "ChangeMe123!"
    from app.core import security
    new_user = User(
        email=email,
        hashed_password=security.get_password_hash("ChangeMe123!"),
        organization_id=current_user.organization_id,
        role=role,
        is_active=True
    )
    db.add(new_user)
    await db.commit()
    return {"message": "User created/invited successfully"}

@router.get("/my-org")
async def get_my_org(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user's organization details.
    """
    result = await db.execute(select(Organization).where(Organization.id == current_user.organization_id))
    org = result.scalars().first()
    return org
