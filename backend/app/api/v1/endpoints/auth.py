from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.core import security
from app.core.config import settings
from app.services.auth import authenticate_user
from app.schemas.token import Token
from app.schemas.user import UserCreate, User as UserSchema
from app.services.user import create_user
from app.services.fingerprint import FingerprintService
from app.services.anomaly import AnomalyService
from app.services.risk import RiskEngine

router = APIRouter()

# @router.post("/login", response_model=Token)
# async def login_access_token(
#     request: Request,
#     db: AsyncSession = Depends(get_db),
#     form_data: OAuth2PasswordRequestForm = Depends()
# ) -> Any:
#     """
#     OAuth2 compatible token login with Risk-Based Authentication (Module C).
#     Includes:
#     - Module A: Behavioral Anomaly Detection
#     - Module B: Device Fingerprinting
#     - Module C: Risk Aggregation & Policy Enforcement
#     """
#     user = await authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect email or password")
#     
#     if not user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
# 
#     # --- Risk Analysis ---
#     ip_address = request.client.host if request.client else "0.0.0.0"
#     user_agent = request.headers.get("user-agent", "unknown")
#     
#     # 1. Module B: Device Check
#     fp_service = FingerprintService(db)
#     device_result = await fp_service.check_device(
#         user_id=user.id,
#         user_agent=user_agent,
#         ip_address=ip_address
#     )
#     
#     # 2. Module A: Anomaly Check
#     anomaly_service = AnomalyService(db)
#     anomaly_result = await anomaly_service.detect_login_anomaly(
#         org_id=user.organization_id if user.organization_id else 1, # Fallback
#         user_id=user.id,
#         login_time=datetime.utcnow(),
#         ip_address=ip_address
#     )
#     # Update baseline async (sync here for MVP)
#     await anomaly_service.update_login_baseline(
#         org_id=user.organization_id if user.organization_id else 1,
#         user_id=user.id,
#         login_time=datetime.utcnow(),
#         ip_address=ip_address
#     )
# 
#     # 3. Module C: Risk Engine
#     risk_engine = RiskEngine(db)
#     risk_calculation = await risk_engine.calculate_risk(
#         user=user,
#         ip_address=ip_address,
#         device_result=device_result,
#         anomaly_result=anomaly_result
#     )
#     risk_score = risk_calculation["total_score"]
#     policy_decision = await risk_engine.decide_policy(user.organization_id, risk_score)
#     
#     # --- Enforcement ---
#     if policy_decision == "BLOCK":
#         # Log this blocking event?
#         raise HTTPException(
#             status_code=403, 
#             detail=f"Login blocked due to high risk ({risk_score}). Factors: {risk_calculation['factors']}"
#         )
#     
#     elif policy_decision == "MFA":
#         # In a real app, verifying MFA code would happen here or return a temp token.
#         # For this MVP, we will ALLOW but warn in the response, OR strictly require it.
#         # Let's SIMULATE MFA Requirement by checking a header 'x-mfa-code'
#         # If missing, return 401 MFA_REQUIRED
#         
#         mfa_code = request.headers.get("x-mfa-code")
#         # For MVP, we will just log/warn. In production, uncomment the raise.
#         if not mfa_code:
#              # raise HTTPException(
#              #    status_code=401, 
#              #    detail="MFA Required",
#              #    headers={"WW-Authenticate": "MFA realm=\"Generic\""}
#              # )
#              print("MFA would be required here (Risk Decision: MFA). Skipping for MVP.")
#         # If code exists, assume valid for MVP demo
#     
#     # ---------------------
# 
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = security.create_access_token(
#         user.id, expires_delta=access_token_expires, role=user.role, org_id=user.organization_id
#     )
#     
#     return {
#         "access_token": access_token,
#         "token_type": "bearer",
#         "risk_score": risk_score,
#         "risk_factors": risk_calculation["factors"]
#     }

@router.post("/register", response_model=UserSchema)
async def register_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user and organization.
    """
    # Check if user exists
    result = await db.execute(select(UserSchema).where(UserSchema.email == user_in.email)) # Fix: Use correct Model
    # Logic is fine, but lets stick to Service Pattern if possible or Raw SQL
    # Re-using previous logic but fixing imports if needed
    
    # ... (Keep existing simple logic for brevity, assuming standard imports in auth.py are enough)
    from app.models.user import User as UserModel
    from app.models.organization import Organization as OrgModel
    
    # Check User
    res = await db.execute(select(UserModel).where(UserModel.email == user_in.email))
    if res.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check Org
    res = await db.execute(select(OrgModel).where(OrgModel.name == user_in.organization_name))
    if res.scalars().first():
        raise HTTPException(status_code=400, detail="Organization name taken")

    # Create
    org = OrgModel(name=user_in.organization_name, subscription_plan="trial")
    db.add(org)
    await db.flush()
    
    user = UserModel(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role="org_admin",
        organization_id=org.id
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
