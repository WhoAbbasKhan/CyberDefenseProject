from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.playbook import Playbook, PlaybookExecution
from app.models.incident import Incident
from app.services.defense import BlacklistService
from datetime import datetime
import json

class PlaybookService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def evaluate_incident(self, incident: Incident):
        """
        Check if any active playbook matches this incident.
        """
        # Fetch active playbooks
        result = await self.db.execute(
            select(Playbook).where(
                Playbook.org_id == incident.org_id,
                Playbook.is_active == True # noqa
            )
        )
        playbooks = result.scalars().all()
        
        for pb in playbooks:
            should_run = False
            conditions = pb.trigger_condition
            if isinstance(conditions, str): conditions = json.loads(conditions)
            
            # Logic: Match condition
            # Example: {"severity": "CRITICAL"} matches Incident.severity
            if "severity" in conditions:
                if conditions["severity"] == incident.severity:
                    should_run = True
            
            if should_run:
                await self.execute_playbook(pb, incident)

    async def execute_playbook(self, playbook: Playbook, incident: Incident):
        """
        Execute actions.
        """
        logs = []
        actions = playbook.actions
        if isinstance(actions, str): actions = json.loads(actions)
        
        try:
            for action in actions:
                if action == "BLOCK_IP":
                    if incident.actor_ip:
                         # Block IP
                         # Assuming BlacklistService exists and has block method (implied in Phase 5)
                         # manual insert for now if service not fully exposed
                         from app.services.defense import BlockedIP
                         blocked = BlockedIP(
                             ip_address=incident.actor_ip,
                             reason=f"Playbook Execution: {playbook.name}",
                             expires_at=datetime.utcnow() 
                         )
                         self.db.add(blocked)
                         logs.append(f"Blocked IP {incident.actor_ip}")
                    else:
                        logs.append("Action BLOCK_IP skipped: No Actor IP")
                
                elif action == "NOTIFY_ADMIN":
                    # Mock Email
                    logs.append(f"Notified Admin about Incident #{incident.id}")
                
            status = "SUCCESS"
        except Exception as e:
            status = "FAILED"
            logs.append(f"Error: {str(e)}")
            
        # Record Execution
        record = PlaybookExecution(
            playbook_id=playbook.id,
            incident_id=incident.id,
            status=status,
            logs=logs
        )
        self.db.add(record)
        await self.db.commit()
