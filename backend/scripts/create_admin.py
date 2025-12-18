from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.models.device import UserDevice
from app.models.behavior import BehavioralProfile, AnomalyEvent
from app.models.incident import Incident
from app.models.organization import Organization
from app.core.security import get_password_hash
from sqlalchemy.future import select
import asyncio
import sys

# Windows requires this for asyncio loop
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def create_admin():
    async with AsyncSessionLocal() as session:
        print("Creating admin user...")
        
        # Check if org exists or create one
        org_res = await session.execute(select(Organization).where(Organization.name == "Velvet Astro HQ"))
        org = org_res.scalars().first()
        
        if not org:
            org = Organization(name="Velvet Astro HQ", subscription_plan="enterprise")
            session.add(org)
            await session.commit()
            await session.refresh(org)
            print(f"Created Organization: {org.name}")
        else:
            print(f"Organization exists: {org.name}")

        # Check if user exists
        user_res = await session.execute(select(User).where(User.email == "admin@velvetastro.io"))
        existing_user = user_res.scalars().first()
        
        if existing_user:
            print("User admin@velvetastro.io already exists. Updating password...")
            existing_user.hashed_password = get_password_hash("admin123")
            session.add(existing_user)
        else:
            print("Creating new user admin@velvetastro.io...")
            user = User(
                email="admin@velvetastro.io",
                hashed_password=get_password_hash("admin123"),
                full_name="Admin User",
                role="super_admin",
                is_active=True,
                organization_id=org.id
            )
            session.add(user)
        
        await session.commit()
        print("Admin user seeded successfully.")

if __name__ == "__main__":
    asyncio.run(create_admin())
