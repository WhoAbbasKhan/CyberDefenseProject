import asyncio
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash
from app.models.organization import Organization

async def create_admin():
    async with AsyncSessionLocal() as db:
        # Check if org exists
        org = await db.get(Organization, 1)
        if not org:
            print("Creating default Org...")
            org = Organization(id=1, name="Velvet Corp", plan="ENTERPRISE", is_active=True)
            db.add(org)
            await db.commit()
        
        # Check if user exists
        user = await db.get(User, 1)
        if not user:
            print("Creating Admin User...")
            user = User(
                id=1,
                email="admin@velvet.net",
                full_name="Admin User",
                hashed_password=get_password_hash("admin"),
                role="SUPER_ADMIN",
                org_id=1,
                is_active=True
            )
            db.add(user)
            await db.commit()
            print("Admin User Created.")
        else:
            print("Admin User already exists.")

if __name__ == "__main__":
    asyncio.run(create_admin())
