from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.forensic import ForensicEvidence
from app.models.incident import Incident
import hashlib
import json
from datetime import datetime

class ForensicService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_evidence(self, org_id: int, evidence_type: str, data: dict, incident_id: int = None) -> ForensicEvidence:
        """
        Log immutable evidence.
        1. Serialize data.
        2. Fetch last hash for chain.
        3. Compute new hash.
        4. Save.
        """
        # Serialize
        data_str = json.dumps(data, sort_keys=True)
        
        # Get last hash (Chain of Custody)
        # In a real blockchain, we'd link to the very last global block or per-org block.
        # Here: Per-Org Chain
        result = await self.db.execute(
            select(ForensicEvidence)
            .where(ForensicEvidence.org_id == org_id)
            .order_by(ForensicEvidence.id.desc())
            .limit(1)
        )
        last_record = result.scalars().first()
        prev_hash = last_record.cryptographic_hash if last_record else "GENESIS_HASH"
        
        # Compute Hash
        # SHA256(prev_hash + type + data + timestamp_approx)
        # Timestamp is tricky if DB generates it. We'll generate it here or trust the commit.
        # For strictness: We hash data + prev_hash. Timestamp is metadata.
        payload = f"{prev_hash}|{evidence_type}|{data_str}".encode()
        curr_hash = hashlib.sha256(payload).hexdigest()
        
        evidence = ForensicEvidence(
            org_id=org_id,
            incident_id=incident_id,
            evidence_type=evidence_type,
            data=data,
            cryptographic_hash=curr_hash,
            previous_hash=prev_hash
        )
        self.db.add(evidence)
        await self.db.commit()
        await self.db.refresh(evidence)
        return evidence

    async def verify_chain(self, org_id: int) -> dict:
        """
        Walk the chain and verify hashes.
        Returns: { "valid": bool, "broken_at_id": int }
        """
        result = await self.db.execute(
            select(ForensicEvidence)
            .where(ForensicEvidence.org_id == org_id)
            .order_by(ForensicEvidence.id.asc())
        )
        chain = result.scalars().all()
        
        prev_hash = "GENESIS_HASH"
        for item in chain:
            # Re-compute
            data_str = json.dumps(item.data, sort_keys=True)
            payload = f"{prev_hash}|{item.evidence_type}|{data_str}".encode()
            calc_hash = hashlib.sha256(payload).hexdigest()
            
            if calc_hash != item.cryptographic_hash:
                return { "valid": False, "broken_at_id": item.id, "reason": "Hash Mismatch" }
            
            if item.previous_hash != prev_hash:
                return { "valid": False, "broken_at_id": item.id, "reason": "Chain Link Broken" }
                
            prev_hash = item.cryptographic_hash
            
        return { "valid": True, "count": len(chain) }

    async def get_timeline(self, incident_id: int):
        result = await self.db.execute(
            select(ForensicEvidence)
            .where(ForensicEvidence.incident_id == incident_id)
            .order_by(ForensicEvidence.timestamp.asc())
        )
        return result.scalars().all()
