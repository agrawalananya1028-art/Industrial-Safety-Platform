"""Alert API Routes"""

from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.alert import AlertSchema
from app.services import alert as alert_service

router = APIRouter()


@router.get("/", response_model=List[AlertSchema])
async def list_alerts(db: Session = Depends(get_db), status: str = None, severity: str = None, limit: int = 50):
    """List alerts with optional filtering"""
    alerts = await alert_service.list_alerts(db, status, severity, limit)
    return alerts


@router.get("/active")
async def get_active_alerts(db: Session = Depends(get_db)) -> List[AlertSchema]:
    """Get active alerts"""
    alerts = await alert_service.get_active_alerts(db)
    return alerts


@router.get("/{alert_id}", response_model=AlertSchema)
async def get_alert(alert_id: UUID, db: Session = Depends(get_db)):
    """Get alert details"""
    alert = await alert_service.get_alert(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.post("/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: UUID, acknowledged_by: UUID, db: Session = Depends(get_db)):
    """Acknowledge an alert"""
    alert = await alert_service.acknowledge_alert(db, alert_id, acknowledged_by)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"status": "acknowledged", "alert_id": alert_id}


@router.post("/{alert_id}/resolve")
async def resolve_alert(alert_id: UUID, resolved_by: UUID, notes: str, db: Session = Depends(get_db)):
    """Resolve an alert"""
    alert = await alert_service.resolve_alert(db, alert_id, resolved_by, notes)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"status": "resolved", "alert_id": alert_id}
