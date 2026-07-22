"""Permit API Routes"""

from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.permit import PermitSchema, PermitCreate, PermitValidationRequest, PermitValidationResponse
from app.services import permit as permit_service
from app.agents.coordinator import coordinator_agent

router = APIRouter()


@router.post("/", response_model=PermitSchema)
async def create_permit(permit_data: PermitCreate, db: Session = Depends(get_db)):
    """Create a new work permit"""
    permit = await permit_service.create_permit(db, permit_data)
    return permit


@router.get("/", response_model=List[PermitSchema])
async def list_permits(db: Session = Depends(get_db), status: str = None, permit_type: str = None):
    """List permits with optional filtering"""
    permits = await permit_service.list_permits(db, status, permit_type)
    return permits


@router.get("/active")
async def get_active_permits(db: Session = Depends(get_db)) -> List[PermitSchema]:
    """Get active permits"""
    permits = await permit_service.get_active_permits(db)
    return permits


@router.get("/{permit_id}", response_model=PermitSchema)
async def get_permit(permit_id: UUID, db: Session = Depends(get_db)):
    """Get permit details"""
    permit = await permit_service.get_permit(db, permit_id)
    if not permit:
        raise HTTPException(status_code=404, detail="Permit not found")
    return permit


@router.post("/validate", response_model=PermitValidationResponse)
async def validate_permit(validation_request: PermitValidationRequest, db: Session = Depends(get_db)):
    """Validate permit using AI agent"""
    result = await coordinator_agent.validate_permit(db, validation_request)
    return result


@router.post("/{permit_id}/approve")
async def approve_permit(permit_id: UUID, reason: str, approved_by: UUID, db: Session = Depends(get_db)):
    """Approve a permit"""
    permit = await permit_service.approve_permit(db, permit_id, reason, approved_by)
    if not permit:
        raise HTTPException(status_code=404, detail="Permit not found")
    return {"status": "approved", "permit_id": permit_id}


@router.post("/{permit_id}/reject")
async def reject_permit(permit_id: UUID, reason: str, rejected_by: UUID, db: Session = Depends(get_db)):
    """Reject a permit"""
    permit = await permit_service.reject_permit(db, permit_id, reason, rejected_by)
    if not permit:
        raise HTTPException(status_code=404, detail="Permit not found")
    return {"status": "rejected", "permit_id": permit_id}
