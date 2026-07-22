"""Risk Assessment Model"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, UUID as UUIDType, Integer, Float, Text, Index
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSONB
import enum

from app.database import Base


class RiskLevel(str, enum.Enum):
    SAFE = "safe"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskAssessment(Base):
    """Risk Assessment Model"""

    __tablename__ = "risk_assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Location
    location_zone = Column(String(100), nullable=False, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Risk Score
    risk_score = Column(Integer, nullable=False, index=True)  # 0-100
    risk_level = Column(ENUM(RiskLevel), nullable=False, index=True)
    
    # Components
    sensor_risk = Column(Integer, default=0)  # Risk from sensor readings
    worker_risk = Column(Integer, default=0)  # Risk from worker location/PPE
    permit_risk = Column(Integer, default=0)  # Risk from permit status
    weather_risk = Column(Integer, default=0)  # Risk from weather conditions
    maintenance_risk = Column(Integer, default=0)  # Risk from maintenance status
    historical_risk = Column(Integer, default=0)  # Risk from historical patterns
    
    # Risk Factors
    factors = Column(JSONB, default=dict)  # {factor_name: value, ...}
    
    # Explanation
    reasoning = Column(Text, nullable=False)  # AI-generated explanation
    key_risks = Column(JSONB, default=list)  # List of main risk factors
    
    # Recommended Actions
    recommended_actions = Column(JSONB, default=list)  # List of actions
    
    # Triggered Alerts
    triggered_alerts = Column(JSONB, default=list)  # List of alert IDs
    
    # Workers in zone
    workers_in_zone = Column(JSONB, default=list)  # Worker data
    
    # Sensors in zone
    sensors_in_zone = Column(JSONB, default=list)  # Sensor readings
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    __table_args__ = (
        Index("idx_risk_zone_time", "location_zone", "timestamp"),
        Index("idx_risk_level_time", "risk_level", "timestamp"),
    )

    def __repr__(self) -> str:
        return f"<RiskAssessment zone={self.location_zone} score={self.risk_score}>"
