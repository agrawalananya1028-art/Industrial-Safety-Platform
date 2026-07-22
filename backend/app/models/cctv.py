"""CCTV Event Model"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, UUID as UUIDType, Text, Boolean, Index, LargeBinary
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSONB
import enum

from app.database import Base


class CCTVEventType(str, enum.Enum):
    MISSING_HELMET = "missing_helmet"
    MISSING_VEST = "missing_vest"
    MISSING_GLOVES = "missing_gloves"
    RESTRICTED_AREA_ENTRY = "restricted_area_entry"
    FIRE = "fire"
    SMOKE = "smoke"
    CROWD = "crowd"
    WORKER_COLLAPSE = "worker_collapse"
    EQUIPMENT_HAZARD = "equipment_hazard"
    FALL_RISK = "fall_risk"


class CCTVEventSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CCTVEvent(Base):
    """CCTV Detection Event Model"""

    __tablename__ = "cctv_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Camera info
    camera_id = Column(String(100), nullable=False, index=True)
    camera_zone = Column(String(100), nullable=False)
    
    # Event details
    event_type = Column(ENUM(CCTVEventType), nullable=False, index=True)
    severity = Column(ENUM(CCTVEventSeverity), nullable=False)
    confidence = Column(float, default=0.0)  # 0-1 confidence score
    
    # Description
    description = Column(Text, nullable=False)
    details = Column(JSONB, default=dict)  # Additional detection details
    
    # People detected
    people_count = Column(int, default=0)
    person_ids = Column(JSONB, default=list)  # List of detected person IDs
    
    # Snapshot
    snapshot_path = Column(String(500), nullable=True)  # Path to image file
    snapshot_data = Column(LargeBinary, nullable=True)  # Base64 encoded image
    
    # Alert
    alert_generated = Column(Boolean, default=False, index=True)
    alert_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Review
    reviewed = Column(Boolean, default=False)
    reviewed_by = Column(UUID(as_uuid=True), nullable=True)
    review_notes = Column(Text, nullable=True)
    false_positive = Column(Boolean, default=False)
    
    # Timestamp
    event_timestamp = Column(DateTime, nullable=False, index=True)
    detected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        Index("idx_cctv_camera_time", "camera_id", "event_timestamp"),
        Index("idx_cctv_type_severity", "event_type", "severity"),
        Index("idx_cctv_zone", "camera_zone"),
    )

    def __repr__(self) -> str:
        return f"<CCTVEvent {self.event_type} - {self.severity}>"
