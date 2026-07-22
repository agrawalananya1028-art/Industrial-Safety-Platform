"""Compliance Service"""

from uuid import UUID
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from app.models import ComplianceRecord
from app.models.compliance import ComplianceStatus


async def get_overall_score(db: Session) -> Dict[str, Any]:
    """Get overall compliance score"""
    total_records = db.query(ComplianceRecord).count()
    if total_records == 0:
        return {"overall_score": 0, "details": {}}
    
    compliant = db.query(ComplianceRecord).filter(
        ComplianceRecord.status == ComplianceStatus.COMPLIANT
    ).count()
    
    overall_score = (compliant / total_records * 100) if total_records > 0 else 0
    
    return {
        "overall_score": round(overall_score, 2),
        "total_records": total_records,
        "compliant_records": compliant,
        "non_compliant_records": total_records - compliant
    }


async def list_records(db: Session, compliance_type: Optional[str] = None, status: Optional[str] = None) -> List[ComplianceRecord]:
    """List compliance records"""
    query = db.query(ComplianceRecord)
    if compliance_type:
        query = query.filter(ComplianceRecord.compliance_type == compliance_type)
    if status:
        query = query.filter(ComplianceRecord.status == status)
    
    return query.order_by(ComplianceRecord.updated_at.desc()).all()


async def get_record(db: Session, record_id: UUID) -> Optional[ComplianceRecord]:
    """Get compliance record by ID"""
    return db.query(ComplianceRecord).filter(ComplianceRecord.id == record_id).first()


async def get_open_issues(db: Session) -> List[Dict[str, Any]]:
    """Get open compliance issues"""
    records = db.query(ComplianceRecord).filter(
        ComplianceRecord.status.in_([ComplianceStatus.NON_COMPLIANT, ComplianceStatus.WARNING])
    ).all()
    
    return [
        {
            "id": str(record.id),
            "category": record.category,
            "status": record.status,
            "issue_count": len(record.pending_issues or [])
        }
        for record in records
    ]


async def run_audit(db: Session) -> Dict[str, Any]:
    """Run compliance audit"""
    # Simulate audit logic
    return {
        "audit_timestamp": "2024-01-01T00:00:00Z",
        "total_items_checked": 50,
        "compliant_items": 47,
        "non_compliant_items": 3,
        "compliance_percentage": 94.0
    }
