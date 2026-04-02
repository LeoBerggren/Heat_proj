from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket_manager import manager

router = APIRouter()

@router.websocket("/ws/heat/{heat_id}")
async def websocket_endpoint(websocket: WebSocket, heat_id: int):
    await manager.connect(heat_id, websocket)
    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        manager.disconnect(heat_id, websocket)

