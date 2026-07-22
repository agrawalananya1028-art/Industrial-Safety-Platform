"""Machine/Equipment Model"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, UUID as UUIDType, Boolean, Float, Text, Index
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSONB
import enum

from app.database import Base


class MachineStatus(str, enum.Enum):
    OPERATIONAL = "operational"
    MAINTENANCE = "maintenance"
    IDLE = "idle"
    FAULTY = "faulty"
    DECOMMISSIONED = "decommissioned"


class Machine(Base):
    """Equipment/Machine Model"""

    __tablename__ = "machines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    machine_code = Column(String(100), unique=True, nullable=False)
    machine_type = Column(String(100), nullable=False)
    
    # Location
    location_zone = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Status
    status = Column(ENUM(MachineStatus), default=MachineStatus.OPERATIONAL, index=True)
    health_score = Column(Float, default=100.0)  # 0-100
    
    # Specifications
    manufacturer = Column(String(255), nullable=True)
    model = Column(String(255), nullable=True)
    serial_number = Column(String(100), nullable=True)
    installation_date = Column(DateTime, nullable=True)
    
    # Safety
    hazard_category = Column(String(100), nullable=True)  # e.g., high-pressure, electrical
    safety_features = Column(String(1000), nullable=True)  # CSV list
    guard_present = Column(Boolean, default=True)
    emergency_stop_present = Column(Boolean, default=True)
    
    # Maintenance
    last_maintenance = Column(DateTime, nullable=True)
    next_maintenance = Column(DateTime, nullable=True)
    maintenance_interval_days = Column(int, default=90)
    maintenance_history = Column(JSONB, default=list)  # List of maintenance records
    
    # Usage
    operating_hours = Column(float, default=0.0)
    last_operated = Column(DateTime, nullable=True)
    cycles_remaining = Column(int, nullable=True)
    
    # Documentation
    manual_link = Column(String(500), nullable=True)
    safety_procedures = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_machine_zone_status", "location_zone", "status"),
        Index("idx_machine_type", "machine_type"),
    )

    def __repr__(self) -> str:
        return f"<Machine {self.name} ({self.status})>"
