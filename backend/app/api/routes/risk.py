"""Risk Assessment API Routes"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.risk import RiskAssessmentResponse
from app.services import risk as risk_service

router = APIRouter()


@router.post("/assess", response_model=RiskAssessmentResponse)
async def assess_risk(location_zone: str, db: Session = Depends(get_db)):
    """Assess risk for a location zone"""
    risk = await risk_service.assess_zone_risk(db, location_zone)
    return risk


@router.get("/zones")
async def get_risk_zones(db: Session = Depends(get_db)):
    """Get current risk levels for all zones"""
    zones = await risk_service.get_all_zones_risk(db)
    return zones


@router.get("/history/{location_zone}")
async def get_risk_history(location_zone: str, db: Session = Depends(get_db), hours: int = 24):
    """Get risk assessment history for a zone"""
    history = await risk_service.get_risk_history(db, location_zone, hours)
    return history
