"""WebSocket Management for Real-time Updates"""

import json
import logging
from typing import Set
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.routing import APIRouter

logger = logging.getLogger(__name__)


class ConnectionManager:
    """WebSocket connection manager"""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.subscriptions: dict = {}  # user_id -> {topics: set}

    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"WebSocket connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Disconnect WebSocket"""
        self.active_connections.discard(websocket)
        logger.info(f"WebSocket disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        for connection in self.active_connections.copy():
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to connection: {e}")
                self.disconnect(connection)

    async def send_to_user(self, user_id: str, message: dict):
        """Send message to specific user"""
        for connection in self.active_connections.copy():
            try:
                await connection.send_json({
                    "type": "user_message",
                    "user_id": user_id,
                    "data": message
                })
            except Exception as e:
                logger.error(f"Error sending to user: {e}")

    async def broadcast_topic(self, topic: str, message: dict):
        """Broadcast to topic subscribers"""
        for connection in self.active_connections.copy():
            try:
                await connection.send_json({
                    "type": "topic_message",
                    "topic": topic,
                    "data": message
                })
            except Exception as e:
                logger.error(f"Error broadcasting topic: {e}")


manager = ConnectionManager()


def setup_websocket(app):
    """Setup WebSocket routes"""
    router = APIRouter()

    @router.websocket("/ws/dashboard")
    async def websocket_dashboard(websocket: WebSocket):
        """WebSocket for real-time dashboard updates"""
        await manager.connect(websocket)
        try:
            while True:
                # Receive subscription requests
                data = await websocket.receive_json()
                if data.get("type") == "subscribe":
                    topic = data.get("topic")
                    logger.info(f"Client subscribed to {topic}")
        except WebSocketDisconnect:
            manager.disconnect(websocket)
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            manager.disconnect(websocket)

    @router.websocket("/ws/alerts")
    async def websocket_alerts(websocket: WebSocket):
        """WebSocket for real-time alerts"""
        await manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_json()
                if data.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
        except WebSocketDisconnect:
            manager.disconnect(websocket)
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            manager.disconnect(websocket)

    app.include_router(router)
