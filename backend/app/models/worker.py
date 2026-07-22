"""Worker Model"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, DateTime, Boolean, Float, Index
from sqlalchemy.dialects.postgresql import UUID, ENUM
import enum

from app.database import Base


class WorkerStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"
    SHIFT_COMPLETE = "shift_complete"


class Worker(Base):
    """Worker (Employee) Model"""

    __tablename__ = "workers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    employee_id = Column(String(100), unique=True, nullable=False)
    department = Column(String(100), nullable=False, index=True)
    role = Column(String(100), nullable=False)
    status = Column(ENUM(WorkerStatus), default=WorkerStatus.ACTIVE, index=True)
    
    # Location data
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    current_zone = Column(String(100), nullable=True)
    
    # Shift info
    shift_id = Column(String(100), nullable=True)
    shift_start = Column(DateTime, nullable=True)
    shift_end = Column(DateTime, nullable=True)
    
    # Safety info
    certifications = Column(String(1000), nullable=True)  # CSV list
    safety_score = Column(Float, default=100.0)
    last_safety_training = Column(DateTime, nullable=True)
    
    # PPE
    helmet_equipped = Column(Boolean, default=False)
    vest_equipped = Column(Boolean, default=False)
    gloves_equipped = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_seen_at = Column(DateTime, nullable=True)
    
    __table_args__ = (
        Index("idx_worker_department_status", "department", "status"),
        Index("idx_worker_location", "latitude", "longitude"),
    )

    def __repr__(self) -> str:
        return f"<Worker {self.name} ({self.employee_id})>"
