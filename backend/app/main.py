"""FastAPI Application Entry Point"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.database import init_db
from app.api import routes
from app.api.websocket import setup_websocket

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager"""
    # Startup
    logger.info("Starting Industrial Safety Intelligence Platform...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title="Industrial Safety Intelligence Platform API",
    description="Real-time industrial safety monitoring and AI-powered risk prediction",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "Industrial Safety Platform"}
    )


# Include API routes
app.include_router(routes.dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(routes.sensors.router, prefix="/api/sensors", tags=["Sensors"])
app.include_router(routes.workers.router, prefix="/api/workers", tags=["Workers"])
app.include_router(routes.permits.router, prefix="/api/permits", tags=["Permits"])
app.include_router(routes.incidents.router, prefix="/api/incidents", tags=["Incidents"])
app.include_router(routes.alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(routes.compliance.router, prefix="/api/compliance", tags=["Compliance"])
app.include_router(routes.risk.router, prefix="/api/risk", tags=["Risk Assessment"])
app.include_router(routes.analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(routes.chat.router, prefix="/api/chat", tags=["Chatbot"])

# Setup WebSocket
setup_websocket(app)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
