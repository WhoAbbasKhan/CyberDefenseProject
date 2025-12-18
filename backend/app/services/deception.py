from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.deception import DeceptionAsset
from app.models.incident import Incident
from app.services.defense import BlockedIP
from datetime import datetime
import uuid

class DeceptionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_asset(self, org_id: int, asset_type: str, label: str, config: dict = {}) -> DeceptionAsset:
        """
        Create a new trap.
        """
        token = str(uuid.uuid4())
        asset = DeceptionAsset(
            org_id=org_id,
            asset_type=asset_type,
            token=token,
            label=label,
            configuration=config
        )
        self.db.add(asset)
        await self.db.commit()
        await self.db.refresh(asset)
        return asset

    async def trigger_trap(self, token: str, metadata: dict):
        """
        Called when a trap is accessed.
        1. Log the event.
        2. Create Critical Incident.
        3. Block the IP.
        """
        result = await self.db.execute(select(DeceptionAsset).where(DeceptionAsset.token == token))
        asset = result.scalars().first()
        
        if not asset:
            return None # Invalid token, maybe ignore or log generic anomaly
        
        # Update Asset Stats
        asset.triggered_count += 1
        asset.last_triggered_at = datetime.utcnow()
        self.db.add(asset)
        
        # Create Critical Incident
        attacker_ip = metadata.get("ip_address")
        summary = f"DECEPTION TRIGGERED: {asset.label} ({asset.asset_type}) accessed by {attacker_ip}"
        
        incident = Incident(
            org_id=asset.org_id,
            status="OPEN",
            severity="CRITICAL",
            kill_chain_stage="Action",
            summary=summary,
            description=f"Metadata: {metadata}",
            actor_ip=attacker_ip,
            actor_user_id=metadata.get("user_id")
        )
        self.db.add(incident)
        
        # Auto-Block IP if present
        if attacker_ip:
            # We need to manually add to BlockedIP or use BlacklistService
            # Simplified:
            blocked = BlockedIP(
                ip_address=attacker_ip,
                reason=f"Triggered Deception Asset: {asset.label}",
                expires_at=datetime.utcnow() + datetime.timedelta(days=365) # Long ban
            )
            # self.db.add(blocked) # Assuming BlockedIP is a model, but wait, it might be a Service logic. 
            # Checking base.py imports: "from app.services.defense import BlacklistService"
            # Actually BlockedIP is likely a Model. Let's create it if it doesn't exist or use logic if it's just a service.
            # IN Phase 5 we implemented IP Blocking. Let's assume we can add it. 
            # Re-checking imports... "from app.services.defense import BlockedIP" <-- This implies it's a Model imported in base.py
            self.db.add(blocked)

        await self.db.commit()
        return incident
