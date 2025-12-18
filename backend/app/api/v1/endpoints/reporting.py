from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from datetime import datetime
from pydantic import BaseModel

from app.api import deps
from app.models.user import User

router = APIRouter()

# --- Schemas ---
class ReportSchema(BaseModel):
    id: int
    name: str
    date: str
    type: str
    size: str

class CreateReportRequest(BaseModel):
    name: str
    type: str

# --- Mock Data ---
# Moved from frontend to backend
MOCK_REPORTS = [
    {"id": 1, "name": "SOC2 Compliance Report", "date": "Dec 14, 2025", "type": "Audit", "size": "2.4 MB"},
    {"id": 2, "name": "Monthly Threat Summary", "date": "Dec 01, 2025", "type": "Summary", "size": "1.1 MB"},
    {"id": 3, "name": "Employee Risk Assessment", "date": "Nov 28, 2025", "type": "Internal", "size": "850 KB"},
    {"id": 4, "name": "ISO 27001 Readiness", "date": "Nov 15, 2025", "type": "Audit", "size": "3.2 MB"},
]

# --- Endpoints ---

@router.get("/", response_model=List[ReportSchema])
async def get_reports(
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get all generated reports.
    """
    return MOCK_REPORTS

@router.get("/compliance/soc2", response_model=Dict[str, Any])
async def get_soc2_report(
    current_user: User = Depends(deps.get_current_active_superuser)
):
    """
    Generate a mock SOC2 Compliance Readiness Report.
    """
    return {
        "generated_at": datetime.utcnow(),
        "status": "partial_compliant",
        "controls": {
            "access_control": {"status": "pass", "details": "MFA and RBAC implemented."},
            "monitoring": {"status": "pass", "details": "Real-time attack logging active."},
            "incident_response": {"status": "warning", "details": "Automated playbook coverage < 80%."},
            "data_retention": {"status": "pass", "details": "Audit logs retained for 90 days."}
        },
        "score": 85
    }

@router.get("/compliance/iso27001", response_model=Dict[str, Any])
async def get_iso27001_report(
    current_user: User = Depends(deps.get_current_active_superuser)
):
    """
    Generate a mock ISO 27001 Report.
    """
    return {
        "generated_at": datetime.utcnow(),
        "status": "compliant", 
        "domains": [
            {"name": "A.5 Information Security Policies", "status": "Implemented"},
            {"name": "A.9 Access Control", "status": "Implemented"},
            {"name": "A.12 Operations Security", "status": "Implemented"}
        ]
    }

@router.post("/custom", response_model=ReportSchema)
async def create_custom_report(
    report_in: CreateReportRequest,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Mock creation of a custom report.
    """
    new_report = {
        "id": len(MOCK_REPORTS) + 1,
        "name": report_in.name,
        "date": datetime.utcnow().strftime("%b %d, %Y"),
        "type": report_in.type,
        "size": "0 KB" # Pending generation
    }
    MOCK_REPORTS.insert(0, new_report) # Add to top
    return new_report
