"""Incident API Routes"""

from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.incident import IncidentSchema, IncidentCreate
from app.services import incident as incident_service

router = APIRouter()


@router.post("/", response_model=IncidentSchema)
async def create_incident(incident_data: IncidentCreate, db: Session = Depends(get_db)):
    """Create an incident report"""
    incident = await incident_service.create_incident(db, incident_data)
    return incident


@router.get("/", response_model=List[IncidentSchema])
async def list_incidents(db: Session = Depends(get_db), severity: str = None, days: int = 30):
    """List incidents with optional filtering"""
    incidents = await incident_service.list_incidents(db, severity, days)
    return incidents


@router.get("/{incident_id}", response_model=IncidentSchema)
async def get_incident(incident_id: UUID, db: Session = Depends(get_db)):
    """Get incident details"""
    incident = await incident_service.get_incident(db, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.get("/similar/{incident_id}")
async def get_similar_incidents(incident_id: UUID, db: Session = Depends(get_db), limit: int = 5) -> List[IncidentSchema]:
    """Get similar past incidents using RAG"""
    similar = await incident_service.get_similar_incidents(db, incident_id, limit)
    return similar


@router.post("/{incident_id}/analyze")
async def analyze_incident(incident_id: UUID, db: Session = Depends(get_db)):
    """Analyze incident with AI agent"""
    analysis = await incident_service.analyze_incident(db, incident_id)
    return analysis
