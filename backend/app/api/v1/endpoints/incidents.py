from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from datetime import datetime, timedelta
from app.api.deps import get_db, get_current_user
from app.services.kill_chain import KillChainService
from app.models.incident import Incident
from app.models.user import User
from app.models.web_event import WebEvent
from app.models.email_event import EmailEvent

router = APIRouter()

@router.post("/correlate", status_code=200)
async def trigger_correlation(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Manually trigger Kill Chain analysis for the organization.
    Useful for demo/verification.
    """
    service = KillChainService(db)
    await service.correlate_events(current_user.org_id if current_user.org_id else 1)
    return {"message": "Correlation analysis started"}

@router.get("/stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get dashboard metrics (mocked/aggregated).
    """
    # In a real scenario, this would aggregate db queries.
    # For MVP, we'll return dynamic-ish mock data to match the Frontend UI needs.
    
    # 1. Time Range (Last 24h)
    now = datetime.utcnow()
    last_24h = now - timedelta(hours=24)
    
    # 2. Active Threats (High/Critical Web + Email Events in last 24h)
    # We could also include "Incidents" table, but let's focus on raw detection events for "Active Threats"
    
    # Web Threats
    res_web_threats = await db.execute(
        select(func.count(WebEvent.id)).where(
            WebEvent.timestamp >= last_24h,
            WebEvent.severity.in_(["high", "critical"])
        )
    )
    web_threat_count = res_web_threats.scalar() or 0
    
    # Email Threats
    res_email_threats = await db.execute(
        select(func.count(EmailEvent.id)).where(
            EmailEvent.detected_at >= last_24h,
            EmailEvent.severity.in_(["high", "critical"])
        )
    )
    email_threat_count = res_email_threats.scalar() or 0
    
    active_threats = web_threat_count + email_threat_count
    
    # 3. Critical Incidents (From Incidents Table or Critical Events)
    # Let's count "critical" detected events for now as "Critical Incidents" metric
    res_crit_web = await db.execute(
        select(func.count(WebEvent.id)).where(
            WebEvent.timestamp >= last_24h,
            WebEvent.severity == "critical"
        )
    )
    res_crit_email = await db.execute(
        select(func.count(EmailEvent.id)).where(
            EmailEvent.detected_at >= last_24h,
            EmailEvent.severity == "critical"
        )
    )
    critical_incidents = (res_crit_web.scalar() or 0) + (res_crit_email.scalar() or 0)
    
    # 4. Global Traffic (Total Web Requests in last 24h)
    res_total_web = await db.execute(
        select(func.count(WebEvent.id)).where(WebEvent.timestamp >= last_24h)
    )
    total_reqs = res_total_web.scalar() or 0
    # Approx req/min
    req_per_min = int(total_reqs / (24 * 60)) if total_reqs > 0 else 0
    
    # 5. Chart Data (Attacks over time - grouped by 4h blocks for simplicity, or just raw hours)
    # For simplicity in this async setup without complex group by syntax flexibility across DBs (sqlite vs pg), 
    # we might fetch attacks and process in python or do a simple grouping. 
    # Let's query all attack timestamps in last 24h and bucket in Python.
    
    res_attacks_time = await db.execute(
        select(WebEvent.timestamp).where(
            WebEvent.timestamp >= last_24h,
            WebEvent.attack_type.isnot(None)
        )
    )
    attack_times = res_attacks_time.scalars().all()
    
    # Bucket into 6 4-hour windows
    buckets = {
        "00:00": 0, "04:00": 0, "08:00": 0, "12:00": 0, "16:00": 0, "20:00": 0
    }
    
    for t in attack_times:
        h = t.hour
        if 0 <= h < 4: buckets["00:00"] += 1
        elif 4 <= h < 8: buckets["04:00"] += 1
        elif 8 <= h < 12: buckets["08:00"] += 1
        elif 12 <= h < 16: buckets["12:00"] += 1
        elif 16 <= h < 20: buckets["16:00"] += 1
        else: buckets["20:00"] += 1

    chart_data = [{"name": k, "attacks": v} for k, v in buckets.items()]
    
    # 6. Recent Attacks Feed
    # Fetch top 5 recent from Web and Email, sort and take top 5
    res_recent_web = await db.execute(
        select(WebEvent).where(WebEvent.attack_type.isnot(None))
        .order_by(WebEvent.timestamp.desc()).limit(5)
    )
    recent_web = res_recent_web.scalars().all()
    
    res_recent_email = await db.execute(
        select(EmailEvent).where(EmailEvent.attack_type.isnot(None))
        .order_by(EmailEvent.detected_at.desc()).limit(5)
    )
    recent_email = res_recent_email.scalars().all()
    
    # Combine and Sort
    combined_feed = []
    for w in recent_web:
        combined_feed.append({
            "id": f"web-{w.id}",
            "type": w.attack_type,
            "target": w.target_url,
            "ip": w.source_ip,
            "severity": w.severity,
            "time": w.timestamp.strftime("%H:%M")
        })
    for e in recent_email:
        combined_feed.append({
            "id": f"email-{e.id}",
            "type": e.attack_type,
            "target": e.recipient_email,
            "ip": e.sender_email, # using sender as IP slot for UI consistency
            "severity": e.severity,
            "time": e.detected_at.strftime("%H:%M")
        })
        
    # Sort by time desc
    combined_feed.sort(key=lambda x: x['time'], reverse=True)
    recent_attacks = combined_feed[:5]

    return {
        "active_threats": active_threats,
        "critical_incidents": critical_incidents,
        "systems_protected": 100, # Mock for now
        "global_traffic": f"{req_per_min} / min",
        "chart_data": chart_data,
        "recent_attacks": recent_attacks
    }

@router.get("/", status_code=200)
async def get_incidents(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List all incidents for the organization.
    """
    result = await db.execute(
        select(Incident).where(Incident.org_id == current_user.org_id)
    )
    incidents = result.scalars().all()
    return incidents
