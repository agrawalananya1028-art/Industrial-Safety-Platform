"""Sensor API Routes"""

from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.sensor import SensorSchema, SensorCreate, SensorReadingSchema, SensorReadingCreate
from app.services import sensor as sensor_service

router = APIRouter()


@router.post("/", response_model=SensorSchema)
async def create_sensor(sensor_data: SensorCreate, db: Session = Depends(get_db)):
    """Create a new sensor"""
    sensor = await sensor_service.create_sensor(db, sensor_data)
    return sensor


@router.get("/", response_model=List[SensorSchema])
async def list_sensors(db: Session = Depends(get_db), zone: str = None, status: str = None):
    """List sensors with optional filtering"""
    sensors = await sensor_service.list_sensors(db, zone, status)
    return sensors


@router.get("/{sensor_id}", response_model=SensorSchema)
async def get_sensor(sensor_id: UUID, db: Session = Depends(get_db)):
    """Get sensor details"""
    sensor = await sensor_service.get_sensor(db, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


@router.post("/{sensor_id}/readings", response_model=SensorReadingSchema)
async def add_sensor_reading(sensor_id: UUID, reading: SensorReadingCreate, db: Session = Depends(get_db)):
    """Add sensor reading"""
    reading.sensor_id = sensor_id
    new_reading = await sensor_service.add_reading(db, reading)
    return new_reading


@router.get("/{sensor_id}/readings", response_model=List[SensorReadingSchema])
async def get_sensor_readings(sensor_id: UUID, db: Session = Depends(get_db), limit: int = 100):
    """Get sensor readings history"""
    readings = await sensor_service.get_readings(db, sensor_id, limit)
    return readings


@router.get("/{sensor_id}/latest")
async def get_latest_reading(sensor_id: UUID, db: Session = Depends(get_db)):
    """Get latest sensor reading"""
    reading = await sensor_service.get_latest_reading(db, sensor_id)
    if not reading:
        raise HTTPException(status_code=404, detail="No readings found")
    return reading
