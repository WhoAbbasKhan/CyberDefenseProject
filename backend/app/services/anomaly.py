import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from sklearn.ensemble import IsolationForest
from app.models.behavior import BehavioralProfile, AnomalyEvent
from app.models.login_event import LoginEvent
from datetime import datetime, timedelta
import json

class AnomalyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_profile(self, org_id: int, entity_type: str, entity_id: str) -> BehavioralProfile:
        result = await self.db.execute(
            select(BehavioralProfile).where(
                BehavioralProfile.org_id == org_id,
                BehavioralProfile.entity_type == entity_type,
                BehavioralProfile.entity_id == entity_id
            )
        )
        profile = result.scalars().first()
        if not profile:
            profile = BehavioralProfile(
                org_id=org_id,
                entity_type=entity_type, 
                entity_id=entity_id,
                baseline_data={"login_times": [], "ip_history": []}
            )
            self.db.add(profile)
            await self.db.commit()
            await self.db.refresh(profile)
        return profile

    async def update_login_baseline(self, org_id: int, user_id: int, login_time: datetime, ip_address: str):
        profile = await self.get_or_create_profile(org_id, "user", str(user_id))
        
        # Parse existing data
        data = profile.baseline_data if profile.baseline_data else {"login_times": [], "ip_history": []}
        if isinstance(data, str):
            data = json.loads(data)
            
        # Update Login Time (Hour of day)
        hour = login_time.hour + (login_time.minute / 60.0)
        login_times = data.get("login_times", [])
        login_times.append(hour)
        
        # Keep last 50 logins
        if len(login_times) > 50:
            login_times = login_times[-50:]
            
        data["login_times"] = login_times
        
        # Update IP History
        ip_history = data.get("ip_history", [])
        if ip_address not in ip_history:
            ip_history.append(ip_address)
        data["ip_history"] = ip_history

        profile.baseline_data = data
        self.db.add(profile)
        await self.db.commit()


    async def detect_login_anomaly(self, org_id: int, user_id: int, login_time: datetime, ip_address: str) -> dict:
        """
        Returns { "is_anomaly": bool, "score": float (0-100), "confidence": float, "reason": str }
        """
        profile = await self.get_or_create_profile(org_id, "user", str(user_id))
        data = profile.baseline_data
        if not data:
            return {"is_anomaly": False, "score": 0.0, "confidence": 0.0, "reason": "No baseline"}

        login_times = data.get("login_times", [])
        
        # Not enough data for ML
        if len(login_times) < 5:
             # Fallback: Simple Heuristic (New IP Check)
             if ip_address not in data.get("ip_history", []):
                 return {"is_anomaly": True, "score": 60.0, "confidence": 0.5, "reason": "New IP Address (Low Baseline)"}
             return {"is_anomaly": False, "score": 0.0, "confidence": 0.0, "reason": "Insufficient data"}

        # Scikit-Learn Isolation Forest
        # Feature: Login Hour
        X = np.array(login_times).reshape(-1, 1)
        clf = IsolationForest(contamination=0.1, random_state=42)
        clf.fit(X)
        
        current_hour = login_time.hour + (login_time.minute / 60.0)
        prediction = clf.predict([[current_hour]]) # 1 = normal, -1 = anomaly
        score = clf.decision_function([[current_hour]]) # Negative scores are anomalies

        anomaly_score = 0.0
        is_anomaly = False
        reason = ""

        if prediction[0] == -1:
            is_anomaly = True
            # Normalize decision function to 0-100 roughly
            # Lower score = more anomalous. Typical range -0.5 to 0.5
            norm_score = abs(score[0]) * 100 
            anomaly_score = min(max(norm_score + 50, 50), 100) # Boost score if anomaly
            reason = f"Unusual Login Time ({int(current_hour)}:00)"
        else:
            anomaly_score = 10.0 # Low risk

        # Factor in IP
        if ip_address not in data.get("ip_history", []):
            anomaly_score += 30
            reason += " & New IP" if reason else "New IP Address"
            is_anomaly = True

        result = {
            "is_anomaly": is_anomaly,
            "score": min(anomaly_score, 100.0),
            "confidence": 0.8 if len(login_times) > 20 else 0.4,
            "reason": reason
        }

        if is_anomaly:
             # Log Anomaly Event
             event = AnomalyEvent(
                 org_id=org_id,
                 event_type="login_anomaly",
                 severity_score=result["score"],
                 confidence_score=result["confidence"],
                 details={"user_id": user_id, "ip": ip_address, "reason": reason}
             )
             self.db.add(event)
             await self.db.commit()

        return result
