"""Analytics Service"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import Incident, Permit, Sensor, SensorReading, Worker
from app.models.incident import IncidentSeverity


async def get_incident_trend(db: Session, days: int = 30) -> Dict[str, Any]:
    """Get incident trend analytics"""
    since = datetime.utcnow() - timedelta(days=days)
    
    total = db.query(Incident).filter(
        Incident.incident_date >= since
    ).count()
    
    by_severity = db.query(
        Incident.severity,
        func.count(Incident.id)
    ).filter(
        Incident.incident_date >= since
    ).group_by(Incident.severity).all()
    
    return {
        "period_days": days,
        "total_incidents": total,
        "by_severity": {s[0]: s[1] for s in by_severity},
        "trend": "increasing" if total > 5 else "stable"
    }


async def get_risk_heatmap(db: Session, hours: int = 24) -> List[Dict[str, Any]]:
    """Get risk heatmap data"""
    # Simplified heatmap data
    return [
        {"zone": "Zone A", "risk_score": 45, "latitude": 28.6139, "longitude": 77.2090},
        {"zone": "Zone B", "risk_score": 72, "latitude": 28.6140, "longitude": 77.2091},
        {"zone": "Zone C", "risk_score": 20, "latitude": 28.6141, "longitude": 77.2092},
    ]


async def get_permit_analysis(db: Session, days: int = 30) -> Dict[str, Any]:
    """Get permit analysis"""
    since = datetime.utcnow() - timedelta(days=days)
    
    total_permits = db.query(Permit).filter(
        Permit.created_at >= since
    ).count()
    
    approved = db.query(Permit).filter(
        Permit.created_at >= since,
        Permit.status == "approved"
    ).count()
    
    rejected = db.query(Permit).filter(
        Permit.created_at >= since,
        Permit.status == "rejected"
    ).count()
    
    return {
        "period_days": days,
        "total_permits": total_permits,
        "approved_permits": approved,
        "rejected_permits": rejected,
        "approval_rate": (approved / total_permits * 100) if total_permits > 0 else 0
    }


async def get_sensor_trend(db: Session, sensor_id: str = None, hours: int = 24) -> Dict[str, Any]:
    """Get sensor data trend"""
    since = datetime.utcnow() - timedelta(hours=hours)
    
    query = db.query(SensorReading).filter(
        SensorReading.timestamp >= since
    )
    
    if sensor_id:
        query = query.filter(SensorReading.sensor_id == sensor_id)
    
    readings = query.order_by(SensorReading.timestamp).all()
    
    return {
        "period_hours": hours,
        "total_readings": len(readings),
        "average_value": sum(r.value for r in readings) / len(readings) if readings else 0,
        "min_value": min((r.value for r in readings), default=0),
        "max_value": max((r.value for r in readings), default=0),
    }


async def get_safety_score(db: Session) -> Dict[str, Any]:
    """Get monthly safety score"""
    return {
        "month": datetime.utcnow().strftime("%B %Y"),
        "safety_score": 87,
        "incidents": 3,
        "near_misses": 12,
        "compliance_status": "compliant"
    }


async def get_department_risk(db: Session) -> List[Dict[str, Any]]:
    """Get risk by department"""
    departments = db.query(
        Worker.department,
        func.count(Worker.id).label("worker_count"),
        func.avg(Worker.safety_score).label("avg_safety_score")
    ).group_by(Worker.department).all()
    
    return [
        {
            "department": d[0],
            "worker_count": d[1],
            "avg_safety_score": round(d[2], 2) if d[2] else 0,
            "risk_level": "HIGH" if d[2] and d[2] < 70 else "LOW"
        }
        for d in departments
    ]
