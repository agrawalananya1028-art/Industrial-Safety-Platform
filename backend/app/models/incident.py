"""Incident Model"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, UUID as UUIDType, Text, Index, Integer, Float
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSONB, ARRAY
import enum

from app.database import Base


class IncidentSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    FATAL = "fatal"


class IncidentType(str, enum.Enum):
    MINOR_INJURY = "minor_injury"
    SERIOUS_INJURY = "serious_injury"
    FATALITY = "fatality"
    NEAR_MISS = "near_miss"
    PROPERTY_DAMAGE = "property_damage"
    ENVIRONMENTAL = "environmental"
    CHEMICAL_SPILL = "chemical_spill"
    FIRE = "fire"
    EXPLOSION = "explosion"
    ELECTRICAL = "electrical"
    FALL = "fall"
    CRUSH = "crush"


class Incident(Base):
    """Incident/Accident Report Model"""

    __tablename__ = "incidents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_number = Column(String(50), unique=True, nullable=False, index=True)
    incident_type = Column(ENUM(IncidentType), nullable=False, index=True)
    severity = Column(ENUM(IncidentSeverity), nullable=False, index=True)
    
    # Timing
    incident_date = Column(DateTime, nullable=False, index=True)
    reported_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Location
    location_zone = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Description
    description = Column(Text, nullable=False)
    sequence_of_events = Column(Text, nullable=True)
    
    # People involved
    workers_involved = Column(ARRAY(UUID(as_uuid=True)), nullable=True)
    injuries_count = Column(Integer, default=0)
    fatalities_count = Column(Integer, default=0)
    
    # Root cause
    root_cause = Column(Text, nullable=True)
    root_cause_category = Column(String(100), nullable=True)
    contributing_factors = Column(ARRAY(String(100)), nullable=True)
    
    # Investigation
    investigated_by = Column(UUID(as_uuid=True), nullable=True)
    investigation_date = Column(DateTime, nullable=True)
    investigation_findings = Column(Text, nullable=True)
    
    # Prevention
    preventive_actions = Column(JSONB, default=dict)  # {action: status, ...}
    corrective_actions = Column(JSONB, default=dict)
    
    # Pattern matching
    pattern_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    similar_incidents = Column(ARRAY(UUID(as_uuid=True)), nullable=True)
    
    # Regulatory
    regulatory_requirement = Column(String(500), nullable=True)
    reportable = Column(bool, default=False)
    reported_to_authority = Column(bool, default=False)
    
    # Status
    status = Column(String(50), default="open", index=True)
    closed_date = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_incident_type_severity", "incident_type", "severity"),
        Index("idx_incident_date", "incident_date"),
        Index("idx_incident_zone", "location_zone"),
    )

    def __repr__(self) -> str:
        return f"<Incident {self.incident_number} ({self.incident_type})>"
