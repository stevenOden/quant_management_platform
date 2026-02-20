from fastapi import APIRouter
from starlette.websockets import WebSocket

router = APIRouter()
@router.websocket("/ws/dashbaord")
async def dashboard_ws(websocket: WebSocket):
    await websocket.accept()