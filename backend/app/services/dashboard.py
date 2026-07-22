"""Service Layer - Dashboard Service"""

from datetime import datetime, timedelta
from typing import Dict, Any, List
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Worker, Alert, Sensor, Permit, Incident
from app.models.worker import WorkerStatus
from app.models.alert import AlertStatus, AlertSeverity
from app.models.sensor import SensorStatus
from app.models.permit import PermitStatus


async def get_dashboard_kpis(db: Session) -> Dict[str, Any]:
    """Get dashboard KPIs"""
    now = datetime.utcnow()
    
    # Workers online
    workers_online = db.query(Worker).filter(
        Worker.status == WorkerStatus.ACTIVE
    ).count()
    
    # Sensors active
    sensors_active = db.query(Sensor).filter(
        Sensor.status == SensorStatus.ACTIVE
    ).count()
    
    # Active alerts
    active_alerts = db.query(Alert).filter(
        Alert.status == AlertStatus.ACTIVE
    ).count()
    
    # Critical alerts
    critical_alerts = db.query(Alert).filter(
        Alert.status == AlertStatus.ACTIVE,
        Alert.severity == AlertSeverity.CRITICAL
    ).count()
    
    # Active permits
    active_permits = db.query(Permit).filter(
        Permit.status == PermitStatus.ACTIVE,
        Permit.expires_at > now
    ).count()
    
    # Incidents today
    today = datetime.utcnow().date()
    incidents_today = db.query(Incident).filter(
        func.date(Incident.incident_date) == today
    ).count()
    
    # Incidents this month
    month_start = now.replace(day=1)
    incidents_month = db.query(Incident).filter(
        Incident.incident_date >= month_start
    ).count()
    
    return {
        "workers_online": workers_online,
        "sensors_active": sensors_active,
        "active_alerts": active_alerts,
        "critical_alerts": critical_alerts,
        "active_permits": active_permits,
        "incidents_today": incidents_today,
        "incidents_month": incidents_month,
        "timestamp": now
    }


async def get_active_alerts(db: Session, limit: int = 10) -> List[Dict[str, Any]]:
    """Get active alerts"""
    alerts = db.query(Alert).filter(
        Alert.status == AlertStatus.ACTIVE
    ).order_by(
        Alert.severity.desc(),
        Alert.created_at.desc()
    ).limit(limit).all()
    
    return [
        {
            "id": str(alert.id),
            "type": alert.alert_type,
            "severity": alert.severity,
            "title": alert.title,
            "message": alert.message,
            "location": alert.location_zone,
            "created_at": alert.created_at
        }
        for alert in alerts
    ]


async def get_risk_zones(db: Session) -> List[Dict[str, Any]]:
    """Get current risk zones"""
    # This would typically query the risk_assessment table
    # For now returning mock data structure
    return [
        {
            "zone": "Zone A",
            "risk_score": 75,
            "risk_level": "HIGH",
            "workers_count": 12,
            "alert_count": 3
        }
    ]


async def get_worker_locations(db: Session) -> List[Dict[str, Any]]:
    """Get real-time worker locations"""
    workers = db.query(Worker).filter(
        Worker.status == WorkerStatus.ACTIVE
    ).all()
    
    return [
        {
            "id": str(worker.id),
            "name": worker.name,
            "latitude": worker.latitude,
            "longitude": worker.longitude,
            "zone": worker.current_zone,
            "status": worker.status,
            "helmet": worker.helmet_equipped,
            "vest": worker.vest_equipped
        }
        for worker in workers
        if worker.latitude and worker.longitude
    ]


async def get_sensor_status(db: Session) -> Dict[str, Any]:
    """Get sensor network status"""
    total_sensors = db.query(Sensor).count()
    active_sensors = db.query(Sensor).filter(
        Sensor.status == SensorStatus.ACTIVE
    ).count()
    sensors_in_maintenance = db.query(Sensor).filter(
        Sensor.status == SensorStatus.MAINTENANCE
    ).count()
    failed_sensors = db.query(Sensor).filter(
        Sensor.status == SensorStatus.FAILED
    ).count()
    
    return {
        "total": total_sensors,
        "active": active_sensors,
        "maintenance": sensors_in_maintenance,
        "failed": failed_sensors,
        "uptime_percentage": (active_sensors / total_sensors * 100) if total_sensors > 0 else 0
    }


async def get_active_permits(db: Session) -> List[Dict[str, Any]]:
    """Get active permits"""
    now = datetime.utcnow()
    permits = db.query(Permit).filter(
        Permit.status == PermitStatus.ACTIVE,
        Permit.expires_at > now
    ).order_by(Permit.expires_at).all()
    
    return [
        {
            "id": str(permit.id),
            "number": permit.permit_number,
            "type": permit.permit_type,
            "zone": permit.location_zone,
            "expires_at": permit.expires_at,
            "requested_by": str(permit.requested_by)
        }
        for permit in permits
    ]


async def get_incidents_count(db: Session, days: int = 30) -> Dict[str, Any]:
    """Get incident count for period"""
    since = datetime.utcnow() - timedelta(days=days)
    
    total = db.query(Incident).filter(
        Incident.incident_date >= since
    ).count()
    
    critical = db.query(Incident).filter(
        Incident.incident_date >= since,
        Incident.severity == "critical"
    ).count()
    
    return {
        "period_days": days,
        "total_incidents": total,
        "critical_incidents": critical,
        "near_misses": db.query(Incident).filter(
            Incident.incident_date >= since,
            Incident.incident_type == "near_miss"
        ).count()
    }


async def get_compliance_score(db: Session) -> Dict[str, Any]:
    """Get overall compliance score"""
    return {
        "overall_score": 87,
        "oisd_compliance": 92,
        "dgms_compliance": 85,
        "factory_act_compliance": 88,
        "iso_45001_compliance": 84
    }
