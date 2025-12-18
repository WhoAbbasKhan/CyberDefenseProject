from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from app.models.incident import Incident
from app.models.persona import AttackerPersona
from datetime import datetime
import json

class ProfilingService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_profiles(self, org_id: int):
        """
        Cluster incidents into Personas.
        Logic: Group by Actor IP.
        """
        # Fetch Incidents
        result = await self.db.execute(
            select(Incident).where(
                Incident.org_id == org_id,
                Incident.actor_ip.isnot(None)
            )
        )
        incidents = result.scalars().all()
        
        for inc in incidents:
            ip = inc.actor_ip
            
            # Find existing Persona with this IP
            # In a real graph DB this is easier. Here we scan JSON or just check simplified linkage.
            # Simplified: Check if any persona has this IP in 'related_ips'
            # OR Check if incident is already linked
            
            # Optimization: Fetch all personas first
            res_p = await self.db.execute(select(AttackerPersona).where(AttackerPersona.org_id == org_id))
            personas = res_p.scalars().all()
            
            target_persona = None
            
            for p in personas:
                p_ips = p.related_ips if p.related_ips else []
                if isinstance(p_ips, str): p_ips = json.loads(p_ips)
                
                if ip in p_ips:
                    target_persona = p
                    break
            
            if target_persona:
                # Update Existing
                p_incidents = target_persona.related_incidents if target_persona.related_incidents else []
                if isinstance(p_incidents, str): p_incidents = json.loads(p_incidents)
                
                if inc.id not in p_incidents:
                    p_incidents.append(inc.id)
                    target_persona.related_incidents = p_incidents
                    target_persona.last_seen = datetime.utcnow()
                    self.db.add(target_persona)
            else:
                # Create New Persona
                new_names_count = len(personas) + 1
                new_persona = AttackerPersona(
                    org_id=org_id,
                    name=f"Subnet-Actor-{new_names_count}", # Temporary name
                    sophistication="UNKNOWN",
                    related_ips=[ip],
                    related_incidents=[inc.id],
                    current_status="ACTIVE",
                    description=f"Auto-generated profile based on IP {ip}"
                )
                self.db.add(new_persona)
        
        await self.db.commit()

    async def get_personas(self, org_id: int):
        result = await self.db.execute(
            select(AttackerPersona).where(AttackerPersona.org_id == org_id)
        )
        return result.scalars().all()
