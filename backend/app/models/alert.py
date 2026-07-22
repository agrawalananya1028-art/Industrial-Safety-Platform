"""Alert Model"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, UUID as UUIDType, Text, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSONB
import enum

from app.database import Base


class AlertSeverity(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class AlertStatus(str, enum.Enum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


class AlertType(str, enum.Enum):
    SENSOR_THRESHOLD = "sensor_threshold"
    COMPOUND_RISK = "compound_risk"
    PERMIT_VIOLATION = "permit_violation"
    COMPLIANCE_ISSUE = "compliance_issue"
    PPE_VIOLATION = "ppe_violation"
    UNAUTHORIZED_ENTRY = "unauthorized_entry"
    EQUIPMENT_FAILURE = "equipment_failure"
    EMERGENCY = "emergency"


class Alert(Base):
    """Alert Model"""

    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alert_type = Column(ENUM(AlertType), nullable=False, index=True)
    severity = Column(ENUM(AlertSeverity), nullable=False, index=True)
    status = Column(ENUM(AlertStatus), default=AlertStatus.ACTIVE, index=True)
    
    # Content
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    
    # Context
    source = Column(String(100), nullable=True)  # e.g., "sensor_123", "permit_456"
    context = Column(JSONB, default=dict)  # Additional context data
    
    # Location
    location_zone = Column(String(100), nullable=True)
    latitude = Column(float, nullable=True)
    longitude = Column(float, nullable=True)
    
    # People affected
    workers_affected = Column(String(1000), nullable=True)  # CSV list
    
    # Actions
    recommended_actions = Column(JSONB, default=dict)  # {action: priority, ...}
    action_taken = Column(Text, nullable=True)
    
    # Escalation
    escalated = Column(Boolean, default=False)
    escalated_to = Column(String(100), nullable=True)  # e.g., "safety_officer", "plant_head"
    escalated_at = Column(DateTime, nullable=True)
    
    # Acknowledgment
    acknowledged_by = Column(UUID(as_uuid=True), nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)
    
    # Resolution
    resolved_by = Column(UUID(as_uuid=True), nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    resolution_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_alert_severity_status", "severity", "status"),
        Index("idx_alert_created_at", "created_at"),
        Index("idx_alert_location", "location_zone"),
    )

    def __repr__(self) -> str:
        return f"<Alert {self.alert_type} - {self.severity}>"
