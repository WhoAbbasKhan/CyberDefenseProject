from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.incident import Incident
from app.models.prediction import AttackPrediction
from datetime import datetime, timedelta

class PredictionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_forecast(self, org_id: int):
        """
        Heuristic-based forecasting for MVP.
        """
        now = datetime.utcnow()
        # Look back 30 days
        window_start = now - timedelta(days=30)
        
        # Fetch Stats
        result = await self.db.execute(
            select(Incident).where(
                Incident.org_id == org_id,
                Incident.created_at >= window_start
            )
        )
        incidents = result.scalars().all()
        
        # Aggregation
        phishing_count = 0
        brute_force_count = 0
        anomalies_count = 0 
        
        for inc in incidents:
            summary = inc.summary.lower()
            if "phishing" in summary: phishing_count += 1
            if "brute force" in summary or "login" in summary: brute_force_count += 1
            if "anomaly" in summary: anomalies_count += 1
            
        # Logic: Predict Future
        new_preds = []
        
        if phishing_count > 2:
            new_preds.append({
                "type": "Targeted Phishing",
                "target": "Finance Dept", # Mock inference
                "prob": 75.0,
                "horizon": "48h"
            })
            
        if brute_force_count > 5:
             new_preds.append({
                "type": "Credential Stuffing",
                "target": "Admin Users",
                "prob": 90.0,
                "horizon": "24h"
            })
            
        if anomalies_count > 3:
             new_preds.append({
                "type": "Insider Threat Action",
                "target": "Database",
                "prob": 60.0, 
                "horizon": "7d"
            })

        # Persist Predictions
        for p in new_preds:
             # Check if exists (debounce)
             # ... Logic skipped for brevity ...
             
             pred = AttackPrediction(
                 org_id=org_id,
                 predicted_attack_type=p["type"],
                 target_asset=p["target"],
                 probability=p["prob"],
                 time_horizon=p["horizon"],
                 status="PENDING"
             )
             self.db.add(pred)
             
        await self.db.commit()

    async def get_active_predictions(self, org_id: int):
        result = await self.db.execute(
            select(AttackPrediction).where(
                AttackPrediction.org_id == org_id,
                AttackPrediction.status == "PENDING"
            )
        )
        return result.scalars().all()
