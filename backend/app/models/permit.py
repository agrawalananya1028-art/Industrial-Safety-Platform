"""Permit Model"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, DateTime, UUID as UUIDType, Boolean, Text, Index, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSONB
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class PermitType(str, enum.Enum):
    HOT_WORK = "hot_work"
    CONFINED_SPACE = "confined_space"
    ELECTRICAL = "electrical"
    HEIGHT_WORK = "height_work"
    ISOLATION = "isolation"
    EXCAVATION = "excavation"
    SCAFFOLDING = "scaffolding"


class PermitStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Permit(Base):
    """Work Permit Model"""

    __tablename__ = "permits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    permit_number = Column(String(50), unique=True, nullable=False, index=True)
    permit_type = Column(ENUM(PermitType), nullable=False, index=True)
    
    # Requestor & Approval
    requested_by = Column(UUID(as_uuid=True), nullable=False, index=True)  # Worker ID
    approved_by = Column(UUID(as_uuid=True), nullable=True)  # Supervisor/Manager ID
    
    # Timing
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Location
    location_zone = Column(String(100), nullable=False)
    latitude = Column(float, nullable=True)
    longitude = Column(float, nullable=True)
    
    # Status
    status = Column(ENUM(PermitStatus), default=PermitStatus.PENDING, index=True)
    
    # Conditions & Safety
    conditions = Column(JSONB, default=dict)  # Safety conditions
    required_ppe = Column(String(255), nullable=True)  # CSV list
    supervision_required = Column(Boolean, default=False)
    isolation_required = Column(Boolean, default=False)
    ventilation_required = Column(Boolean, default=False)
    fire_watch_required = Column(Boolean, default=False)
    
    # Approval/Rejection Reason
    approval_reason = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    # AI Validation
    ai_validation_result = Column(JSONB, nullable=True)  # Result from AI permit agent
    ai_checked_at = Column(DateTime, nullable=True)
    
    # Sensor readings at approval time
    sensor_snapshot = Column(JSONB, default=dict)  # Current sensor values
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_permit_type_status", "permit_type", "status"),
        Index("idx_permit_expires", "expires_at"),
        Index("idx_permit_requested_by", "requested_by"),
    )

    def __repr__(self) -> str:
        return f"<Permit {self.permit_number} ({self.permit_type})>"
