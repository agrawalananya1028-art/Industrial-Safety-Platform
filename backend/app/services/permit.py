"""Permit Service"""

from uuid import UUID
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
import secrets
import string

from app.models import Permit
from app.schemas.permit import PermitCreate
from app.models.permit import PermitStatus


def generate_permit_number() -> str:
    """Generate unique permit number"""
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    random_suffix = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    return f"PERMIT-{timestamp}-{random_suffix}"


async def create_permit(db: Session, permit_data: PermitCreate) -> Permit:
    """Create a new permit"""
    permit = Permit(
        permit_number=generate_permit_number(),
        **permit_data.dict()
    )
    db.add(permit)
    db.commit()
    db.refresh(permit)
    return permit


async def list_permits(db: Session, status: Optional[str] = None, permit_type: Optional[str] = None) -> List[Permit]:
    """List permits with optional filtering"""
    query = db.query(Permit)
    if status:
        query = query.filter(Permit.status == status)
    if permit_type:
        query = query.filter(Permit.permit_type == permit_type)
    return query.order_by(Permit.created_at.desc()).all()


async def get_permit(db: Session, permit_id: UUID) -> Optional[Permit]:
    """Get permit by ID"""
    return db.query(Permit).filter(Permit.id == permit_id).first()


async def get_active_permits(db: Session) -> List[Permit]:
    """Get active permits"""
    now = datetime.utcnow()
    return db.query(Permit).filter(
        Permit.status == PermitStatus.ACTIVE,
        Permit.expires_at > now
    ).all()


async def approve_permit(db: Session, permit_id: UUID, reason: str, approved_by: UUID) -> Optional[Permit]:
    """Approve a permit"""
    permit = await get_permit(db, permit_id)
    if not permit:
        return None
    
    permit.status = PermitStatus.APPROVED
    permit.approval_reason = reason
    permit.approved_by = approved_by
    
    db.commit()
    db.refresh(permit)
    return permit


async def reject_permit(db: Session, permit_id: UUID, reason: str, rejected_by: UUID) -> Optional[Permit]:
    """Reject a permit"""
    permit = await get_permit(db, permit_id)
    if not permit:
        return None
    
    permit.status = PermitStatus.REJECTED
    permit.rejection_reason = reason
    permit.approved_by = rejected_by
    
    db.commit()
    db.refresh(permit)
    return permit


async def activate_permit(db: Session, permit_id: UUID) -> Optional[Permit]:
    """Activate an approved permit"""
    permit = await get_permit(db, permit_id)
    if not permit or permit.status != PermitStatus.APPROVED:
        return None
    
    permit.status = PermitStatus.ACTIVE
    permit.started_at = datetime.utcnow()
    
    db.commit()
    db.refresh(permit)
    return permit


async def complete_permit(db: Session, permit_id: UUID) -> Optional[Permit]:
    """Complete an active permit"""
    permit = await get_permit(db, permit_id)
    if not permit or permit.status != PermitStatus.ACTIVE:
        return None
    
    permit.status = PermitStatus.COMPLETED
    permit.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(permit)
    return permit
