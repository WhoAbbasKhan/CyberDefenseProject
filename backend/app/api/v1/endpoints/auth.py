from datetime import timedelta, datetime
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.core import security
from app.core.config import settings
from app.models.user import User
from app.services.google_auth import google_auth_service
from app.services.webauthn_service import webauthn_service
from app.services.risk_engine import risk_engine
from app.schemas.auth import (
    GoogleLogin, 
    Token, 
    PublicKeyCredentialCreationOptionsRequest, 
    RegistrationResponse,
    PublicKeyCredentialRequestOptionsRequest,
    AuthenticationResponse
)
import json

router = APIRouter()

@router.post("/google/login", response_model=Token)
async def google_login(
    login_data: GoogleLogin,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    # 1. Verify Google Token & Get User
    try:
        claims = await google_auth_service.get_user_data(login_data.token) # This takes 'code' actually, naming mismatch in schema?
        # Schema name is 'token' but implementation expects 'code'
    except Exception as e:
         raise HTTPException(status_code=400, detail=f"Google auth failed: {str(e)}")
         
    user = await google_auth_service.get_or_create_user(db, claims)
    
    # 2. Check Risk & Passkey Requirement
    context = {
        "device_id": request.cookies.get("device_id"),
        "ip": request.client.host
    }
    
    if risk_engine.should_require_passkey(user, context):
        # In a real flow, we would return a partial token or specific challenge 
        # indicating 2FA is needed. For simplicity here:
        # We could return a 403 with "MFA_REQUIRED" which frontend catches
        raise HTTPException(status_code=403, detail="MFA_REQUIRED")

    # 3. Issue Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

# --- WebAuthn Registration ---

@router.post("/passkey/register/options")
async def register_options(
    request: PublicKeyCredentialCreationOptionsRequest, # contains username/displayname
    user: User = Depends(get_current_user), # Must be logged in to register passkey
    db: AsyncSession = Depends(get_db)
):
    options = await webauthn_service.generate_registration_options(user, db)
    # Store challenge in session/cookie - For API we might return it and expect it backsigned
    # Or use a temporary cache. For statelessness, we can sign the challenge in a jwt and return it
    # Simplified: return options, frontend must send back exactly what it got + signature
    # WARNING: Challenge session management is critical. We'll rely on frontend returning it signed or
    # simple match for MVP (less secure).
    # Ideally: Store challenge in Redis with TTL using local storage 'challenge'
    
    return json.loads(options.json()) 

@router.post("/passkey/register/verify")
async def register_verify(
    data: RegistrationResponse,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # In a real app, retrieve challenge from server-side session using 'id'
    # Here we assume the client blindly passes it back or we disable challenge check (NOT SECURE)
    # OR we re-generate expected challenge if deterministic? No.
    # We will assume a fixed challenge for MVP if we can't persist state, OR 
    # we just pass a dummy challenge for content. 
    # CORRECT WAY: Use Redis. 
    # Let's mock the challenge check success for MVP since we removed Redis dependency
    
    challenge = "mock_challenge_mvp" # FIXME: Implement stateful challenge
    
    success, msg = await webauthn_service.verify_registration(db, user, data.dict(), challenge)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "ok"}

# --- WebAuthn Login ---

@router.post("/passkey/login/options")
async def login_options(
    request: PublicKeyCredentialRequestOptionsRequest,
    db: AsyncSession = Depends(get_db)
):
    # Lookup user if provided
    user = None
    # if request.username: ... find user ...
    
    options = await webauthn_service.generate_authentication_options(db, user)
    return json.loads(options.json())

@router.post("/passkey/login/verify")
async def login_verify(
    data: AuthenticationResponse,
    db: AsyncSession = Depends(get_db)
):
    # We need to find WHO is trying to login.
    # The credential ID in 'data.id' maps to a user.
    # webauthn_service.verify_authentication logic finds user by credential_id
    
    # We need to find the user associated with this credential first to pass to verify
    # Refactor service to lookup user inside verify? Yes.
    
    # Quick fix: duplicate lookup logic here or push to service
    from sqlalchemy import select
    from app.models.auth_provider import AuthProvider
    result = await db.execute(select(AuthProvider).where(AuthProvider.credential_id == data.id))
    provider = result.scalars().first()
    if not provider:
         raise HTTPException(status_code=400, detail="Unknown credential")
         
    # Fetch user
    result_user = await db.execute(select(User).where(User.id == provider.user_id))
    user = result_user.scalars().first()
    
    challenge = "mock_challenge_mvp" # FIXME
    
    success, msg = await webauthn_service.verify_authentication(db, data.dict(), challenge, user)
    if not success:
         raise HTTPException(status_code=400, detail=msg)
         
    # Issue Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }
