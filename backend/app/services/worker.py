"""Worker Service"""

from uuid import UUID
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models import Worker
from app.schemas.worker import WorkerCreate, WorkerUpdate


async def create_worker(db: Session, worker_data: WorkerCreate) -> Worker:
    """Create a new worker"""
    worker = Worker(**worker_data.dict())
    db.add(worker)
    db.commit()
    db.refresh(worker)
    return worker


async def list_workers(db: Session, department: Optional[str] = None, status: Optional[str] = None) -> List[Worker]:
    """List workers with optional filtering"""
    query = db.query(Worker)
    if department:
        query = query.filter(Worker.department == department)
    if status:
        query = query.filter(Worker.status == status)
    return query.all()


async def get_worker(db: Session, worker_id: UUID) -> Optional[Worker]:
    """Get worker by ID"""
    return db.query(Worker).filter(Worker.id == worker_id).first()


async def update_worker(db: Session, worker_id: UUID, worker_data: WorkerUpdate) -> Optional[Worker]:
    """Update worker information"""
    worker = await get_worker(db, worker_id)
    if not worker:
        return None
    
    update_data = worker_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(worker, field, value)
    
    db.commit()
    db.refresh(worker)
    return worker


async def get_location(db: Session, worker_id: UUID) -> Optional[dict]:
    """Get worker location"""
    worker = await get_worker(db, worker_id)
    if not worker:
        return None
    return {
        "worker_id": str(worker.id),
        "latitude": worker.latitude,
        "longitude": worker.longitude,
        "zone": worker.current_zone,
        "last_seen": worker.last_seen_at
    }


async def update_location(db: Session, worker_id: UUID, latitude: float, longitude: float) -> Optional[Worker]:
    """Update worker location"""
    from datetime import datetime
    worker = await get_worker(db, worker_id)
    if not worker:
        return None
    
    worker.latitude = latitude
    worker.longitude = longitude
    worker.last_seen_at = datetime.utcnow()
    
    # Determine zone based on coordinates (simplified)
    # In production, use geospatial queries
    if latitude and longitude:
        worker.current_zone = "Zone A"  # Placeholder
    
    db.commit()
    db.refresh(worker)
    return worker


async def get_workers_in_zone(db: Session, zone: str) -> List[Worker]:
    """Get all workers in a zone"""
    return db.query(Worker).filter(
        Worker.current_zone == zone,
        Worker.status == "active"
    ).all()
