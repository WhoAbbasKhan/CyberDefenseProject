from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.services.prediction import PredictionService
from app.models.user import User

router = APIRouter()

@router.post("/forecast", status_code=200)
async def generate_forecast(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger AI forecasting analysis manually.
    """
    service = PredictionService(db)
    await service.generate_forecast(current_user.org_id if current_user.org_id else 1)
    return {"message": "Forecast generation started"}

@router.get("/", status_code=200)
async def get_predictions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get active AI predictions.
    """
    service = PredictionService(db)
    preds = await service.get_active_predictions(current_user.org_id if current_user.org_id else 1)
    return preds
