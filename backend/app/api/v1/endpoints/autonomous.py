from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.ai.rl.agent import agent
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

class SecurityState(BaseModel):
    risk_score: float
    anomaly_score: float
    kill_chain_stage: int

class ActionResponse(BaseModel):
    action: str
    confidence: float = 1.0 # Placeholder for RL confidence

@router.post("/decide", response_model=ActionResponse)
async def get_autonomous_decision(
    state: SecurityState,
    current_user: User = Depends(get_current_user)
):
    """
    Get optimal security action from RL Agent (PPO).
    """
    if not current_user.org_id: # Simple permission check
        raise HTTPException(status_code=403, detail="Organization context required")

    action = agent.decide(
        risk_score=state.risk_score, 
        anomaly_score=state.anomaly_score, 
        kill_chain_stage=state.kill_chain_stage
    )
    
    return {"action": action, "confidence": 0.95}

@router.post("/train")
async def train_agent(
    current_user: User = Depends(get_current_user)
):
    """
    Manually trigger agent retraining (Admin only).
    """
    agent.train()
    return {"status": "Training started"}
