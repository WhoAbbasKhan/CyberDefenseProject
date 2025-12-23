import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import GoogleLogin
from jose import jwt

class GoogleAuthService:
    def __init__(self):
        self.token_url = "https://oauth2.googleapis.com/token"
        self.user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        
    async def get_user_data(self, code: str):
        async with httpx.AsyncClient() as client:
            data = {
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            }
            response = await client.post(self.token_url, data=data)
            response.raise_for_status()
            tokens = response.json()
            id_token = tokens.get("id_token")
            # In prod, verify signature with Google's public keys
            claims = jwt.get_unverified_claims(id_token)
            return claims

    async def get_or_create_user(self, db: AsyncSession, user_data: dict) -> User:
        google_sub = user_data["sub"]
        email = user_data["email"]
        
        # Check by google_sub
        result = await db.execute(select(User).where(User.google_sub == google_sub))
        user = result.scalars().first()
        if user:
            return user
            
        # Check by email
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        if user:
            user.google_sub = google_sub
            await db.commit()
            await db.refresh(user)
            return user
            
        # Create new
        user = User(
            email=email,
            full_name=user_data.get("name"),
            google_sub=google_sub,
            is_active=True,
            role="employee",
            hashed_password=None
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

google_auth_service = GoogleAuthService()
