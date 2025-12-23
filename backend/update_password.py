import asyncio
from app.db.session import AsyncSessionLocal
from app.db.base import Base # Ensure models are registered
from app.models.user import User
from app.models.organization import Organization
from app.core.security import get_password_hash
from sqlalchemy import select

async def update():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).where(User.email == "admin@velvet.com"))
        user = result.scalars().first()
        if user:
            print(f"Updating password for {user.email}")
            # Identify current hash type if possible, or just overwrite
            # print(f"Old hash: {user.hashed_password}")
            user.hashed_password = get_password_hash("password")
            db.add(user)
            await db.commit()
            print("Password updated.")
        else:
            print("User not found.")

if __name__ == "__main__":
    asyncio.run(update())
