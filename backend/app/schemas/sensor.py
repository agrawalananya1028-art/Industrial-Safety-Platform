"""Sensor Schemas"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SensorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    sensor_type: str
    location_zone: str
    unit: str
    min_threshold: Optional[float] = None
    max_threshold: Optional[float] = None
    critical_threshold: Optional[float] = None


class SensorCreate(SensorBase):
    sensor_id: str = Field(..., min_length=1, max_length=100)
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class SensorSchema(SensorBase):
    id: UUID
    sensor_id: str
    latitude: Optional[float]
    longitude: Optional[float]
    status: str
    battery_level: int
    last_reading_value: Optional[float]
    last_reading_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class SensorReadingCreate(BaseModel):
    sensor_id: UUID
    value: float
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None


class SensorReadingSchema(BaseModel):
    id: int
    sensor_id: UUID
    value: float
    unit: str
    is_alert: bool
    is_critical: bool
    timestamp: datetime

    class Config:
        from_attributes = True
