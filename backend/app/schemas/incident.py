"""Incident Schemas"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field


class IncidentBase(BaseModel):
    incident_type: str
    severity: str
    location_zone: str
    description: str = Field(..., min_length=10)
    incident_date: datetime


class IncidentCreate(IncidentBase):
    workers_involved: Optional[List[UUID]] = None
    injuries_count: int = 0
    fatalities_count: int = 0


class IncidentSchema(IncidentBase):
    id: UUID
    incident_number: str
    reported_date: datetime
    latitude: Optional[float]
    longitude: Optional[float]
    workers_involved: Optional[List[UUID]]
    root_cause: Optional[str]
    preventive_actions: dict
    pattern_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
