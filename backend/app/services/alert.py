"""Alert Service"""

from uuid import UUID
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models import Alert
from app.models.alert import AlertStatus


async def list_alerts(db: Session, status: Optional[str] = None, severity: Optional[str] = None, limit: int = 50) -> List[Alert]:
    """List alerts with optional filtering"""
    query = db.query(Alert)
    if status:
        query = query.filter(Alert.status == status)
    if severity:
        query = query.filter(Alert.severity == severity)
    
    return query.order_by(Alert.created_at.desc()).limit(limit).all()


async def get_active_alerts(db: Session) -> List[Alert]:
    """Get active alerts"""
    return db.query(Alert).filter(
        Alert.status == AlertStatus.ACTIVE
    ).order_by(
        Alert.severity.desc(),
        Alert.created_at.desc()
    ).all()


async def get_alert(db: Session, alert_id: UUID) -> Optional[Alert]:
    """Get alert by ID"""
    return db.query(Alert).filter(Alert.id == alert_id).first()


async def create_alert(db: Session, alert_data: dict) -> Alert:
    """Create a new alert"""
    alert = Alert(**alert_data)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


async def acknowledge_alert(db: Session, alert_id: UUID, acknowledged_by: UUID) -> Optional[Alert]:
    """Acknowledge an alert"""
    alert = await get_alert(db, alert_id)
    if not alert:
        return None
    
    alert.status = AlertStatus.ACKNOWLEDGED
    alert.acknowledged_by = acknowledged_by
    alert.acknowledged_at = datetime.utcnow()
    
    db.commit()
    db.refresh(alert)
    return alert


async def resolve_alert(db: Session, alert_id: UUID, resolved_by: UUID, notes: str) -> Optional[Alert]:
    """Resolve an alert"""
    alert = await get_alert(db, alert_id)
    if not alert:
        return None
    
    alert.status = AlertStatus.RESOLVED
    alert.resolved_by = resolved_by
    alert.resolved_at = datetime.utcnow()
    alert.resolution_notes = notes
    
    db.commit()
    db.refresh(alert)
    return alert
