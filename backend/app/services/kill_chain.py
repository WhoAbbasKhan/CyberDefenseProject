from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from app.models.incident import Incident
from app.models.behavior import AnomalyEvent
from app.models.login_event import LoginEvent # Assuming we have this
from datetime import datetime, timedelta
import json

class KillChainService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def correlate_events(self, org_id: int):
        """
        Scan for unlinked patterns in the last 15 minutes.
        Integration Point: This should be run via Celery or Cron.
        For Demo: Triggered manually via API.
        
        Logic:
        1. Find recent Anomaly Events.
        2. See if User/IP has Failed Logins involved.
        3. If Anomaly + Failed Login -> Create/Update Incident.
        """
        now = datetime.utcnow()
        window = now - timedelta(minutes=15)
        
        # 1. Fetch recent critical events (Anomalies)
        result = await self.db.execute(
            select(AnomalyEvent).where(
                AnomalyEvent.org_id == org_id,
                AnomalyEvent.created_at >= window,
                AnomalyEvent.severity_score > 50 # Only high-ish severity
            )
        )
        anomalies = result.scalars().all()
        
        for anomaly in anomalies:
            details = anomaly.details
            if isinstance(details, str):
                details = json.loads(details)
                
            user_id = details.get("user_id")
            ip = details.get("ip")
            
            # 2. Check for correlation (e.g. Existing Incident)
            # Find open incident for this actor
            filters = [Incident.status == "OPEN"]
            if user_id:
                filters.append(Incident.actor_user_id == user_id)
            elif ip:
                filters.append(Incident.actor_ip == ip)
            
            result_inc = await self.db.execute(select(Incident).where(or_(*filters)))
            incident = result_inc.scalars().first()
            
            summary_text = f"Anomaly Detected: {anomaly.event_type} (Score: {anomaly.severity_score})"
            
            if incident:
                # Update existing
                incident.updated_at = now
                incident.severity = "HIGH" if anomaly.severity_score > 80 else incident.severity
                
                # Link event
                current_links = incident.linked_event_ids
                if isinstance(current_links, str): current_links = json.loads(current_links)
                if anomaly.id not in current_links:
                    current_links.append(anomaly.id)
                    incident.linked_event_ids = current_links
                    
                self.db.add(incident)
                
            else:
                # Create NEW Incident
                new_incident = Incident(
                    org_id=org_id,
                    status="OPEN",
                    severity="MEDIUM" if anomaly.severity_score < 80 else "HIGH",
                    kill_chain_stage="EXPLOITATION" if "login" in anomaly.event_type else "RECON",
                    summary=summary_text,
                    actor_ip=ip,
                    actor_user_id=user_id,
                    linked_event_ids=[anomaly.id]
                )
                self.db.add(new_incident)
        
        await self.db.commit()
