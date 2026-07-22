"""API Routes Package"""

from app.api import dashboard, sensors, workers, permits, incidents, alerts, compliance, risk, analytics, chat

__all__ = [
    "dashboard",
    "sensors",
    "workers",
    "permits",
    "incidents",
    "alerts",
    "compliance",
    "risk",
    "analytics",
    "chat",
]
