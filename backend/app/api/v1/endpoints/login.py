import logging
from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.deps import get_db
from app.core import security
from app.core.config import settings
from app.models.user import User
from app.schemas.token import Token

# Setup Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    logger.info(f"Login attempt: {form_data.username}")

    # 1. Database Query
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()

    if not user:
        logger.warning(f"User not found in database: {form_data.username}")
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    logger.info("User found — verifying password")

    # 2. Password Verification (Argon2)
    if not security.verify_password(form_data.password, user.hashed_password):
        logger.warning("Password verification failed")
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not user.is_active:
        logger.warning("User is inactive")
        raise HTTPException(status_code=400, detail="Inactive user")

    logger.info("Password verified — generating JWT")

    # 3. JWT Generation
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    
    logger.info("Login successful — token issued")

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
