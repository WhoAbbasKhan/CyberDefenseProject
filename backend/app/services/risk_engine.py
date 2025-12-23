from sqlalchemy.orm import Session
from app.models.user import User

class RiskEngine:
    def should_require_passkey(self, user: User, context: dict) -> bool:
        """
        Determine if passkey is required based on context (device, location, etc.)
        """
        # 1. Admin always requires passkey
        if user.role in ["super_admin", "org_admin", "security"]:
            return True
            
        # 2. Check device trust (mock implementation)
        # In a real app, we'd check a device cookie or fingerprint against known devices
        device_id = context.get("device_id")
        if not device_id:
            return True # New device -> require strong auth
            
        # 3. Simple risk score (mock)
        # if context.get("risk_score", 0) > 0.7:
        #     return True
            
        return False

risk_engine = RiskEngine()
