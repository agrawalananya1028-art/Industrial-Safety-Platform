"""Risk Assessment Schemas"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID

from pydantic import BaseModel, Field


class RiskAssessmentResponse(BaseModel):
    location_zone: str
    risk_score: int = Field(..., ge=0, le=100)
    risk_level: str
    factors: Dict[str, Any]
    reasoning: str
    key_risks: List[str]
    recommended_actions: List[str]
    timestamp: datetime

    class Config:
        from_attributes = True


class RiskAssessmentSchema(RiskAssessmentResponse):
    id: UUID
    sensor_risk: int
    worker_risk: int
    permit_risk: int
    weather_risk: int
    triggered_alerts: List[str]
