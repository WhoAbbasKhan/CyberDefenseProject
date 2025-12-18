from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.services.defense import DefenseService
from app.models.organization import Organization

class RiskEngine:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.defense_service = DefenseService()

    async def calculate_risk(self, user, ip_address: str, device_result: dict, anomaly_result: dict) -> dict:
        """
        Aggregates risk from various modules.
        Returns { "total_score": int, "factors": list }
        """
        score = 0
        factors = []

        # 1. IP Reputation (Phase 17: Module E + Phase 5)
        # Check Threat Intel
        from app.services.threat import ThreatIntelService
        threat_service = ThreatIntelService(self.db)
        threat_result = await threat_service.check_ip(ip_address)
        
        if threat_result["is_malicious"]:
            ti_score = 50.0 # High penalty for known bad IP
            score += ti_score
            factors.append(f"Threat Intelligence Match ({int(ti_score)} pts): {threat_result.get('description')}")
        
        # 2. Anomaly Detection (Module A)
        anom_score = anomaly_result.get("score", 0)
        if anom_score > 0:
            weighted_anom = anom_score * 0.8 # Weighting
            score += weighted_anom
            if anomaly_result.get("is_anomaly"):
                factors.append(f"Behavioral Anomaly ({int(weighted_anom)} pts): {anomaly_result.get('reason')}")

        # 3. Device Fingerprinting (Module B)
        # device_result = { "is_known": bool, "risk_score": float, ... }
        dev_risk = device_result.get("risk_score", 0)
        if dev_risk > 0:
            score += dev_risk
            factors.append(f"Device Risk ({int(dev_risk)} pts)")

        # Cap score
        total_score = min(score, 100)

        return {
            "total_score": int(total_score),
            "factors": factors
        }

    async def decide_policy(self, org_id: int, risk_score: int) -> str:
        """
        Returns: 'ALLOW', 'MFA', 'BLOCK'
        Future: Fetch from Organization.settings
        """
        # Hardcoded Policy for MVP
        if risk_score >= 80:
            return "BLOCK"
        elif risk_score >= 30:
            return "MFA"
        else:
            return "ALLOW"
