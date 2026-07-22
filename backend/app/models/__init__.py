"""Database Models"""

from app.models.worker import Worker
from app.models.sensor import Sensor, SensorReading
from app.models.permit import Permit
from app.models.incident import Incident
from app.models.alert import Alert
from app.models.risk_assessment import RiskAssessment
from app.models.compliance import ComplianceRecord
from app.models.cctv import CCTVEvent
from app.models.machine import Machine
from app.models.user import User

__all__ = [
    "Worker",
    "Sensor",
    "SensorReading",
    "Permit",
    "Incident",
    "Alert",
    "RiskAssessment",
    "ComplianceRecord",
    "CCTVEvent",
    "Machine",
    "User",
]
