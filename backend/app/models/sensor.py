"""Sensor and SensorReading Models"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey, Index, Boolean
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class SensorType(str, enum.Enum):
    GAS = "gas"
    TEMPERATURE = "temperature"
    PRESSURE = "pressure"
    HUMIDITY = "humidity"
    MOTION = "motion"
    FLAME = "flame"
    SMOKE = "smoke"
    VIBRATION = "vibration"
    PROXIMITY = "proximity"
    LIGHT = "light"


class SensorStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    FAILED = "failed"


class Sensor(Base):
    """IoT Sensor Model"""

    __tablename__ = "sensors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    sensor_id = Column(String(100), unique=True, nullable=False)
    sensor_type = Column(ENUM(SensorType), nullable=False, index=True)
    location_zone = Column(String(100), nullable=False)
    
    # Location
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Configuration
    unit = Column(String(50), nullable=False)  # e.g., ppm, Celsius, bar
    min_threshold = Column(Float, nullable=True)
    max_threshold = Column(Float, nullable=True)
    critical_threshold = Column(Float, nullable=True)
    
    # Status
    status = Column(ENUM(SensorStatus), default=SensorStatus.ACTIVE, index=True)
    battery_level = Column(Integer, default=100)  # percentage
    signal_strength = Column(Integer, nullable=True)  # RSSI
    
    # Last reading
    last_reading_value = Column(Float, nullable=True)
    last_reading_at = Column(DateTime, nullable=True)
    last_alert_at = Column(DateTime, nullable=True)
    
    # Maintenance
    last_maintenance = Column(DateTime, nullable=True)
    next_maintenance = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    readings = relationship("SensorReading", back_populates="sensor", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("idx_sensor_zone_type", "location_zone", "sensor_type"),
        Index("idx_sensor_status", "status"),
    )

    def __repr__(self) -> str:
        return f"<Sensor {self.name} ({self.sensor_type})>"


class SensorReading(Base):
    """Sensor Reading (Time-Series Data) Model"""

    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(UUID(as_uuid=True), ForeignKey("sensors.id"), nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    
    # Status
    is_alert = Column(Boolean, default=False, index=True)
    is_critical = Column(Boolean, default=False, index=True)
    
    # Context
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    pressure = Column(Float, nullable=True)
    
    # Timestamp (indexed for time-series queries)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationship
    sensor = relationship("Sensor", back_populates="readings")
    
    __table_args__ = (
        Index("idx_reading_sensor_time", "sensor_id", "timestamp"),
        Index("idx_reading_alert_time", "is_alert", "timestamp"),
    )

    def __repr__(self) -> str:
        return f"<SensorReading sensor_id={self.sensor_id} value={self.value}>"
