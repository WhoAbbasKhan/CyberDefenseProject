import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.device import UserDevice
from typing import Optional, Dict
from datetime import datetime

class FingerprintService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def generate_hash(self, user_agent: str, ip_address: str, client_data: Optional[Dict] = None) -> str:
        """
        Create a consistent hash from device attributes.
        Ideally uses more client-side signals (screen res, timezone, canvas hash) if available.
        For backend-only scope, we rely on UA + IP (subnet) + provided client hash.
        """
        # Simplified for backend demo: Combine provided headers/IP
        # In prod, IP might change, so we'd rely more on 'client_data' from frontend fingerprintjs
        
        raw_string = f"{user_agent}"
        
        if client_data and "fingerprint" in client_data:
            # If frontend sends a pre-calculated fingerprint (e.g. from FingerprintJS), use it
            raw_string += f"-{client_data['fingerprint']}"
        else:
            # Fallback to backend params
            # We mask IP to /24 to allow minor mobility 
            ip_subnet = ".".join(ip_address.split('.')[:3]) if '.' in ip_address else ip_address
            raw_string += f"-{ip_subnet}"

        return hashlib.sha256(raw_string.encode()).hexdigest()

    async def check_device(self, user_id: int, user_agent: str, ip_address: str, client_data: Optional[Dict] = None) -> dict:
        """
        Returns { "is_known": bool, "risk_score": float, "device_id": int }
        """
        fp_hash = self.generate_hash(user_agent, ip_address, client_data)
        
        # Check if device exists for user
        result = await self.db.execute(
            select(UserDevice).where(
                UserDevice.user_id == user_id,
                UserDevice.fingerprint_hash == fp_hash
            )
        )
        device = result.scalars().first()
        
        if device:
            # Known Device
            device.last_seen_at = datetime.utcnow()
            device.ip_address = ip_address # Update latest IP
            self.db.add(device)
            await self.db.commit()
            
            return {
                "is_known": True,
                "risk_score": 0.0,
                "device_id": device.id,
                "created_at": device.created_at
            }
        else:
            # New Device => High Risk initially? Or just flag it.
            # Create new record (but maybe mark as untrusted until MFA?)
            # For this MVP, we auto-trust but return a Risk Score.
            
            new_device = UserDevice(
                user_id=user_id,
                fingerprint_hash=fp_hash,
                device_name=f"Device ({ip_address})", # In real app, parse UA for "Chrome on Mac"
                ip_address=ip_address,
                user_agent=user_agent,
                is_trusted=True # Auto-trust for now to avoid locking out test user
            )
            self.db.add(new_device)
            await self.db.commit()
            await self.db.refresh(new_device)
            
            return {
                "is_known": False, 
                "risk_score": 30.0, # New Device Penalty
                "device_id": new_device.id,
                "reason": "New Device Detected"
            }
