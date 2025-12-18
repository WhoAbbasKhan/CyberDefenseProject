from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organization import Organization
# We need a BlockedIP model
from app.db.session import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

class BlockedIP(Base):
    __tablename__ = "blocked_ips"
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    ip_address = Column(String, index=True)
    reason = Column(String)
    blocked_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True) # Optional temporary block

class DefenseService:
    async def block_ip(self, db: AsyncSession, org_id: int, ip: str, reason: str):
        # Check if already blocked
        # (Assuming unique constraint or check)
        # For Phase 0, just add
        block = BlockedIP(organization_id=org_id, ip_address=ip, reason=reason)
        db.add(block)
        await db.commit()
    
    async def is_ip_blocked(self, db: AsyncSession, org_id: int, ip: str) -> bool:
        from sqlalchemy import select
        result = await db.execute(select(BlockedIP).where(
            BlockedIP.organization_id == org_id, 
            BlockedIP.ip_address == ip
        ))
        return result.scalars().first() is not None

defense_service = DefenseService()
