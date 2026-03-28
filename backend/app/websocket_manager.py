"""
CityPulse AI — WebSocket Connection Manager
Manages WebSocket connections and broadcasts real-time data to all clients.
"""
import json
from datetime import datetime
from fastapi import WebSocket
from typing import List


class ConnectionManager:
    """
    Manages active WebSocket connections.
    Supports broadcasting sensor data, alerts, and predictions to all clients.
    """

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept and register a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"🔗 Client connected. Active connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove a disconnected client."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        print(f"🔌 Client disconnected. Active connections: {len(self.active_connections)}")

    async def broadcast(self, data: dict):
        """Send data to all connected WebSocket clients."""
        if not self.active_connections:
            return

        # Convert datetime objects for JSON serialization
        message = json.dumps(data, default=str)
        disconnected = []

        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                disconnected.append(connection)

        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)

    async def send_personal(self, websocket: WebSocket, data: dict):
        """Send data to a specific client."""
        try:
            message = json.dumps(data, default=str)
            await websocket.send_text(message)
        except Exception:
            self.disconnect(websocket)

    @property
    def client_count(self) -> int:
        return len(self.active_connections)


# Global connection manager instance
manager = ConnectionManager()
