"""Worker API Routes"""

from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.worker import WorkerSchema, WorkerCreate, WorkerUpdate
from app.services import worker as worker_service

router = APIRouter()


@router.post("/", response_model=WorkerSchema)
async def create_worker(worker_data: WorkerCreate, db: Session = Depends(get_db)):
    """Create a new worker"""
    worker = await worker_service.create_worker(db, worker_data)
    return worker


@router.get("/", response_model=List[WorkerSchema])
async def list_workers(db: Session = Depends(get_db), department: str = None, status: str = None):
    """List workers with optional filtering"""
    workers = await worker_service.list_workers(db, department, status)
    return workers


@router.get("/{worker_id}", response_model=WorkerSchema)
async def get_worker(worker_id: UUID, db: Session = Depends(get_db)):
    """Get worker details"""
    worker = await worker_service.get_worker(db, worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker


@router.put("/{worker_id}", response_model=WorkerSchema)
async def update_worker(worker_id: UUID, worker_data: WorkerUpdate, db: Session = Depends(get_db)):
    """Update worker information"""
    worker = await worker_service.update_worker(db, worker_id, worker_data)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker


@router.get("/location/{worker_id}")
async def get_worker_location(worker_id: UUID, db: Session = Depends(get_db)):
    """Get worker current location"""
    location = await worker_service.get_location(db, worker_id)
    if not location:
        raise HTTPException(status_code=404, detail="Worker not found")
    return location


@router.post("/{worker_id}/location")
async def update_worker_location(worker_id: UUID, latitude: float, longitude: float, db: Session = Depends(get_db)):
    """Update worker location"""
    worker = await worker_service.update_location(db, worker_id, latitude, longitude)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return {"status": "success", "worker_id": worker_id}
