import asyncio
from app.db.session import AsyncSessionLocal
from app.db.base import Base # Register models
from app.models.user import User
from app.models.organization import Organization
from app.core.security import get_password_hash
from sqlalchemy import select

async def create_user():
    async with AsyncSessionLocal() as db:
        # Check if user with ID 1 exists
        result = await db.execute(select(User).where(User.id == 1))
        user = result.scalars().first()
        
        if user:
            print("User with ID 1 already exists.")
            return

        # Check if email exists
        result = await db.execute(select(User).where(User.email == "admin@velvet.com"))
        user = result.scalars().first()
        if user:
             print("User with email already exists.")
             return

        print("Creating user...")
        new_user = User(
            id=1,
            email="admin@velvet.com",
            hashed_password=get_password_hash("password"),
            full_name="Admin User",
            is_active=True,
            role="super_admin",
            organization_id=1 # Assuming Org 1 exists or is nullable/created? 
            # Orgs need to exist too. Let's create mock org if needed or ensure models allow it.
            # User model might have ForeignKey to organizations.id
        )
        
        # Check Org
        # from app.models.organization import Organization
        res_org = await db.execute(select(Organization).where(Organization.id == 1))
        org = res_org.scalars().first()
        if not org:
             print("Creating default organization...")
             new_org = Organization(id=1, name="Velvet Corp", subscription_plan="enterprise", is_trial_active=True)
             db.add(new_org)
             await db.commit()
        
        db.add(new_user)
        await db.commit()
        print("User created successfully.")

if __name__ == "__main__":
    asyncio.run(create_user())
