"""Sensor Service"""

from uuid import UUID
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models import Sensor, SensorReading
from app.schemas.sensor import SensorCreate, SensorReadingCreate


async def create_sensor(db: Session, sensor_data: SensorCreate) -> Sensor:
    """Create a new sensor"""
    sensor = Sensor(**sensor_data.dict())
    db.add(sensor)
    db.commit()
    db.refresh(sensor)
    return sensor


async def list_sensors(db: Session, zone: Optional[str] = None, status: Optional[str] = None) -> List[Sensor]:
    """List sensors with optional filtering"""
    query = db.query(Sensor)
    if zone:
        query = query.filter(Sensor.location_zone == zone)
    if status:
        query = query.filter(Sensor.status == status)
    return query.all()


async def get_sensor(db: Session, sensor_id: UUID) -> Optional[Sensor]:
    """Get sensor by ID"""
    return db.query(Sensor).filter(Sensor.id == sensor_id).first()


async def add_reading(db: Session, reading_data: SensorReadingCreate) -> SensorReading:
    """Add sensor reading"""
    reading = SensorReading(**reading_data.dict())
    db.add(reading)
    db.commit()
    db.refresh(reading)
    
    # Update sensor's last reading
    sensor = await get_sensor(db, reading_data.sensor_id)
    if sensor:
        sensor.last_reading_value = reading.value
        sensor.last_reading_at = reading.timestamp
        db.commit()
    
    return reading


async def get_readings(db: Session, sensor_id: UUID, limit: int = 100) -> List[SensorReading]:
    """Get sensor readings history"""
    return db.query(SensorReading).filter(
        SensorReading.sensor_id == sensor_id
    ).order_by(desc(SensorReading.timestamp)).limit(limit).all()


async def get_latest_reading(db: Session, sensor_id: UUID) -> Optional[SensorReading]:
    """Get latest sensor reading"""
    return db.query(SensorReading).filter(
        SensorReading.sensor_id == sensor_id
    ).order_by(desc(SensorReading.timestamp)).first()


async def get_sensor_readings_by_zone(db: Session, zone: str) -> List[dict]:
    """Get latest readings for all sensors in a zone"""
    sensors = await list_sensors(db, zone=zone)
    readings = []
    for sensor in sensors:
        latest = await get_latest_reading(db, sensor.id)
        if latest:
            readings.append({
                "sensor_id": str(sensor.id),
                "sensor_name": sensor.name,
                "value": latest.value,
                "unit": latest.unit,
                "timestamp": latest.timestamp,
                "is_alert": latest.is_alert,
                "is_critical": latest.is_critical
            })
    return readings
