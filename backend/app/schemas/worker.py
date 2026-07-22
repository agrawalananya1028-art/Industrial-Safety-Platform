"""Worker Schemas"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class WorkerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    employee_id: str = Field(..., min_length=1, max_length=100)
    department: str = Field(..., min_length=1, max_length=100)
    role: str = Field(..., min_length=1, max_length=100)
    shift_start: Optional[datetime] = None
    shift_end: Optional[datetime] = None
    certifications: Optional[str] = None


class WorkerCreate(WorkerBase):
    pass


class WorkerUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    current_zone: Optional[str] = None
    helmet_equipped: Optional[bool] = None
    vest_equipped: Optional[bool] = None
    gloves_equipped: Optional[bool] = None


class WorkerSchema(WorkerBase):
    id: UUID
    status: str
    latitude: Optional[float]
    longitude: Optional[float]
    current_zone: Optional[str]
    safety_score: float
    helmet_equipped: bool
    vest_equipped: bool
    gloves_equipped: bool
    last_seen_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
