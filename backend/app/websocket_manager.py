from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # heat_id -> list of WebSockets
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, heat_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(heat_id, []).append(websocket)

    def disconnect(self, heat_id: int, websocket: WebSocket):
        if heat_id in self.active_connections:
            self.active_connections[heat_id].remove(websocket)

    async def broadcast_to_heat(self, heat_id: int, message: dict):
        for ws in self.active_connections.get(heat_id, []):
            await ws.send_json(message)

manager = ConnectionManager()
