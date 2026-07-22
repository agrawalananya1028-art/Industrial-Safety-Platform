"""Alert Schemas"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID

from pydantic import BaseModel


class AlertBase(BaseModel):
    alert_type: str
    severity: str
    title: str
    message: str
    location_zone: Optional[str] = None


class AlertCreate(AlertBase):
    description: Optional[str] = None
    context: Optional[Dict[str, Any]] = {}
    recommended_actions: Optional[Dict[str, str]] = {}


class AlertSchema(AlertBase):
    id: UUID
    status: str
    source: Optional[str]
    context: Dict[str, Any]
    recommended_actions: Dict[str, str]
    acknowledged_by: Optional[UUID]
    acknowledged_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
