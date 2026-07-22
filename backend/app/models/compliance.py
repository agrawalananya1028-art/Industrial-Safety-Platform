"""Compliance Record Model"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, UUID as UUIDType, Boolean, Text, Index, Integer
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSONB
import enum

from app.database import Base


class ComplianceStatus(str, enum.Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    WARNING = "warning"
    PENDING = "pending"


class ComplianceType(str, enum.Enum):
    OISD = "oisd"  # Oil Industry Safety Directorate
    DGMS = "dgms"  # Directorate General of Mines Safety
    FACTORY_ACT = "factory_act"
    ISO_45001 = "iso_45001"
    INTERNAL_POLICY = "internal_policy"


class ComplianceRecord(Base):
    """Compliance Audit Record Model"""

    __tablename__ = "compliance_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Classification
    compliance_type = Column(ENUM(ComplianceType), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    requirement = Column(String(500), nullable=False)
    
    # Status
    status = Column(ENUM(ComplianceStatus), nullable=False, index=True)
    compliance_score = Column(Integer, default=0)  # 0-100
    
    # Details
    description = Column(Text, nullable=False)
    details = Column(JSONB, default=dict)  # Additional details
    
    # Documentation
    documentation_required = Column(Boolean, default=False)
    documentation_provided = Column(Boolean, default=False)
    document_links = Column(JSONB, default=list)  # List of doc URLs/paths
    
    # Inspection
    last_inspected_by = Column(UUID(as_uuid=True), nullable=True)
    last_inspected_at = Column(DateTime, nullable=True)
    next_inspection_date = Column(DateTime, nullable=True)
    
    # Issues
    issues_found = Column(Integer, default=0)
    issues_resolved = Column(Integer, default=0)
    pending_issues = Column(JSONB, default=list)  # List of open issues
    
    # Certification
    certificate_required = Column(Boolean, default=False)
    certificate_valid_until = Column(DateTime, nullable=True)
    certification_body = Column(String(255), nullable=True)
    
    # Remediation
    remediation_required = Column(Boolean, default=False)
    remediation_plan = Column(Text, nullable=True)
    remediation_deadline = Column(DateTime, nullable=True)
    remediation_completed = Column(Boolean, default=False)
    
    # Owner
    owner = Column(UUID(as_uuid=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_compliance_type_status", "compliance_type", "status"),
        Index("idx_compliance_category", "category"),
        Index("idx_compliance_inspection", "last_inspected_at"),
    )

    def __repr__(self) -> str:
        return f"<ComplianceRecord {self.category} - {self.status}>"
