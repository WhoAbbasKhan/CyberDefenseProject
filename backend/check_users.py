import asyncio
from app.db.base import Base
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.models.organization import Organization
from sqlalchemy import select

async def list_users():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User))
        users = result.scalars().all()
        print(f"Found {len(users)} users:")
        for user in users:
            print(f"ID: {user.id}, Email: {user.email}, Role: {user.role}")

if __name__ == "__main__":
    asyncio.run(list_users())
