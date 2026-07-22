"""User/Administrator Model"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, UUID as UUIDType, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID, ENUM
import enum

from app.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    SAFETY_OFFICER = "safety_officer"
    MANAGER = "manager"
    SUPERVISOR = "supervisor"
    WORKER = "worker"
    AUDITOR = "auditor"
    VIEWER = "viewer"


class User(Base):
    """User/Administrator Model"""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    
    # Authentication
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)
    
    # Authorization
    role = Column(ENUM(UserRole), default=UserRole.VIEWER, index=True)
    
    # Profile
    department = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    
    # Settings
    email_alerts = Column(Boolean, default=True)
    sms_alerts = Column(Boolean, default=False)
    push_alerts = Column(Boolean, default=True)
    
    # Activity
    last_login = Column(DateTime, nullable=True)
    last_activity = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_user_role", "role"),
        Index("idx_user_active", "is_active"),
    )

    def __repr__(self) -> str:
        return f"<User {self.username} ({self.role})>"
