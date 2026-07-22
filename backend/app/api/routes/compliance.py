"""Compliance API Routes"""

from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import compliance as compliance_service

router = APIRouter()


@router.get("/score")
async def get_compliance_score(db: Session = Depends(get_db)):
    """Get overall compliance score"""
    score = await compliance_service.get_overall_score(db)
    return score


@router.get("/records")
async def list_compliance_records(db: Session = Depends(get_db), compliance_type: str = None, status: str = None):
    """List compliance records"""
    records = await compliance_service.list_records(db, compliance_type, status)
    return records


@router.get("/{record_id}")
async def get_compliance_record(record_id: UUID, db: Session = Depends(get_db)):
    """Get compliance record details"""
    record = await compliance_service.get_record(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Compliance record not found")
    return record


@router.get("/issues")
async def get_compliance_issues(db: Session = Depends(get_db)):
    """Get open compliance issues"""
    issues = await compliance_service.get_open_issues(db)
    return issues


@router.post("/audit")
async def run_compliance_audit(db: Session = Depends(get_db)):
    """Run compliance audit"""
    result = await compliance_service.run_audit(db)
    return result
