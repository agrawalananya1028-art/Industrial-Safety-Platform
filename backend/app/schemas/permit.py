"""Permit Schemas"""

from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field


class PermitBase(BaseModel):
    permit_type: str
    location_zone: str
    expires_at: datetime
    conditions: Optional[Dict[str, Any]] = {}
    required_ppe: Optional[str] = None
    supervision_required: bool = False
    isolation_required: bool = False
    ventilation_required: bool = False
    fire_watch_required: bool = False


class PermitCreate(PermitBase):
    requested_by: UUID
    issued_at: Optional[datetime] = None


class PermitSchema(PermitBase):
    id: UUID
    permit_number: str
    requested_by: UUID
    approved_by: Optional[UUID]
    issued_at: datetime
    status: str
    approval_reason: Optional[str]
    rejection_reason: Optional[str]
    ai_validation_result: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PermitValidationRequest(BaseModel):
    permit_id: UUID
    sensor_readings: Optional[Dict[str, float]] = {}
    worker_status: Optional[Dict[str, Any]] = {}
    location_data: Optional[Dict[str, Any]] = {}


class PermitValidationResponse(BaseModel):
    permit_id: UUID
    is_approved: bool
    reasoning: str
    unsafe_conditions: list[str]
    recommendations: list[str]
    sensor_check_passed: bool
    worker_check_passed: bool
    location_check_passed: bool
