"""Dashboard API Routes"""

from datetime import datetime, timedelta
from typing import Dict, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import dashboard as dashboard_service
from app.schemas.risk import RiskAssessmentResponse

router = APIRouter()


@router.get("/kpis")
async def get_dashboard_kpis(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get dashboard KPIs"""
    kpis = await dashboard_service.get_dashboard_kpis(db)
    return kpis


@router.get("/alerts/active")
async def get_active_alerts(db: Session = Depends(get_db), limit: int = 10) -> list:
    """Get active alerts"""
    alerts = await dashboard_service.get_active_alerts(db, limit)
    return alerts


@router.get("/risk-zones")
async def get_risk_zones(db: Session = Depends(get_db)) -> list:
    """Get current risk zones"""
    zones = await dashboard_service.get_risk_zones(db)
    return zones


@router.get("/worker-locations")
async def get_worker_locations(db: Session = Depends(get_db)) -> list:
    """Get real-time worker locations"""
    locations = await dashboard_service.get_worker_locations(db)
    return locations


@router.get("/sensor-status")
async def get_sensor_status(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get sensor network status"""
    status = await dashboard_service.get_sensor_status(db)
    return status


@router.get("/permits-active")
async def get_active_permits(db: Session = Depends(get_db)) -> list:
    """Get active permits"""
    permits = await dashboard_service.get_active_permits(db)
    return permits


@router.get("/incidents-count")
async def get_incidents_count(db: Session = Depends(get_db), days: int = 30) -> Dict[str, Any]:
    """Get incident count for period"""
    count = await dashboard_service.get_incidents_count(db, days)
    return count


@router.get("/compliance-score")
async def get_compliance_score(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get overall compliance score"""
    score = await dashboard_service.get_compliance_score(db)
    return score
