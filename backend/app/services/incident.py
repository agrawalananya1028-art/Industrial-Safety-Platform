"""Incident Service"""

from uuid import UUID
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
import secrets
import string

from app.models import Incident
from app.schemas.incident import IncidentCreate


def generate_incident_number() -> str:
    """Generate unique incident number"""
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    random_suffix = ''.join(secrets.choice(string.digits) for _ in range(4))
    return f"INC-{timestamp}-{random_suffix}"


async def create_incident(db: Session, incident_data: IncidentCreate) -> Incident:
    """Create an incident report"""
    incident = Incident(
        incident_number=generate_incident_number(),
        **incident_data.dict()
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


async def list_incidents(db: Session, severity: Optional[str] = None, days: int = 30) -> List[Incident]:
    """List incidents with optional filtering"""
    since = datetime.utcnow() - timedelta(days=days)
    query = db.query(Incident).filter(Incident.incident_date >= since)
    
    if severity:
        query = query.filter(Incident.severity == severity)
    
    return query.order_by(Incident.incident_date.desc()).all()


async def get_incident(db: Session, incident_id: UUID) -> Optional[Incident]:
    """Get incident by ID"""
    return db.query(Incident).filter(Incident.id == incident_id).first()


async def get_similar_incidents(db: Session, incident_id: UUID, limit: int = 5) -> List[Incident]:
    """Get similar incidents (would use RAG in production)"""
    incident = await get_incident(db, incident_id)
    if not incident:
        return []
    
    # Query similar incidents by type and severity
    return db.query(Incident).filter(
        Incident.incident_type == incident.incident_type,
        Incident.id != incident_id
    ).order_by(Incident.incident_date.desc()).limit(limit).all()


async def analyze_incident(db: Session, incident_id: UUID) -> dict:
    """Analyze incident with AI"""
    incident = await get_incident(db, incident_id)
    if not incident:
        return {"error": "Incident not found"}
    
    return {
        "incident_id": str(incident.id),
        "analysis": "AI analysis would be performed here",
        "root_causes": incident.contributing_factors or [],
        "preventive_actions": incident.preventive_actions or {}
    }
