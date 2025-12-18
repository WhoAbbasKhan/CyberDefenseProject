from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.threat import ThreatIndicator
from datetime import datetime

class ThreatIntelService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def ingest_feed(self, source_name: str, indicators: list):
        """
        Ingest a list of dicts: [ {"value": "1.2.3.4", "type": "IP", "desc": "Bad IP"} ]
        """
        for item in indicators:
            val = item.get("value")
            
            # Check existing
            result = await self.db.execute(select(ThreatIndicator).where(ThreatIndicator.indicator_value == val))
            existing = result.scalars().first()
            
            if existing:
                existing.last_updated = datetime.utcnow()
                existing.source = source_name
            else:
                new_indicator = ThreatIndicator(
                    indicator_value=val,
                    indicator_type=item.get("type", "IP"),
                    source=source_name,
                    description=item.get("desc"),
                    confidence=80.0
                )
                self.db.add(new_indicator)
        
        await self.db.commit()

    async def check_ip(self, ip_address: str) -> dict:
        """
        Returns { "is_malicious": bool, "confidence": float, "source": str }
        """
        result = await self.db.execute(
            select(ThreatIndicator).where(
                ThreatIndicator.indicator_value == ip_address
            )
        )
        indicator = result.scalars().first()
        
        if indicator:
            return {
                "is_malicious": True,
                "confidence": indicator.confidence,
                "source": indicator.source,
                "description": indicator.description
            }
        
        return { "is_malicious": False, "confidence": 0 }
