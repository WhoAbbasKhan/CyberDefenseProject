from fastapi import Depends, HTTPException, status
from app.api import deps
from app.models.user import User
from app.models.organization import Organization
from app.core.subscriptions import get_plan_features, SubscriptionTier
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from sqlalchemy import select

async def check_subscription_active(
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Organization:
    """
    Dependency to verify if the organization's subscription/trial is active.
    """
    result = await db.execute(select(Organization).where(Organization.id == current_user.organization_id))
    org = result.scalars().first()
    
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    # Check Trial Expiry
    if org.subscription_plan == SubscriptionTier.TRIAL:
        if org.trial_end < datetime.utcnow():
             # Mark as expired logic could be here or done by background job
             # For now, just block access
             raise HTTPException(
                 status_code=status.HTTP_402_PAYMENT_REQUIRED,
                 detail="Free trial expired. Please upgrade to continue."
             )
             
    # TODO: Add logic for paid subscription expiry check if we had payment integration
    
    return org

def require_feature(feature_name: str):
    """
    Factory for checking if current org has a specific feature.
    """
    async def feature_checker(org: Organization = Depends(check_subscription_active)):
        features = get_plan_features(org.subscription_plan)
        if "all" not in features.modules and feature_name not in features.modules:
             raise HTTPException(
                 status_code=status.HTTP_403_FORBIDDEN,
                 detail=f"Feature '{feature_name}' not available in current plan."
             )
        return True
    return feature_checker
