"""Analytics API Routes"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import analytics as analytics_service

router = APIRouter()


@router.get("/incidents/trend")
async def get_incident_trend(db: Session = Depends(get_db), days: int = 30):
    """Get incident trend analytics"""
    trend = await analytics_service.get_incident_trend(db, days)
    return trend


@router.get("/risk/heatmap")
async def get_risk_heatmap(db: Session = Depends(get_db), hours: int = 24):
    """Get risk heatmap data"""
    heatmap = await analytics_service.get_risk_heatmap(db, hours)
    return heatmap


@router.get("/permits/analysis")
async def get_permit_analysis(db: Session = Depends(get_db), days: int = 30):
    """Get permit analysis"""
    analysis = await analytics_service.get_permit_analysis(db, days)
    return analysis


@router.get("/sensors/trend")
async def get_sensor_trend(db: Session = Depends(get_db), sensor_id: str = None, hours: int = 24):
    """Get sensor data trend"""
    trend = await analytics_service.get_sensor_trend(db, sensor_id, hours)
    return trend


@router.get("/safety-score")
async def get_monthly_safety_score(db: Session = Depends(get_db)):
    """Get monthly safety score"""
    score = await analytics_service.get_safety_score(db)
    return score


@router.get("/department-risk")
async def get_department_risk(db: Session = Depends(get_db)):
    """Get risk by department"""
    risk = await analytics_service.get_department_risk(db)
    return risk
