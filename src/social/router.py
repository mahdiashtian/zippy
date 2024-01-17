from fastapi import APIRouter, Depends
from fastapi import WebSocket, WebSocketDisconnect
from typing_extensions import Annotated

from src.dependencies import get_current_user_ws
from src.social.exceptions import PermissionDeniedWS
from src.social.manager import ConnectionManager
from src.users import models as user_model

router = APIRouter()
manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket,
                             user: Annotated[user_model.User, Depends(get_current_user_ws)]):
    room = user.room
    if not room:
        raise PermissionDeniedWS
    room_id = room.id
    await manager.connect(room_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "image": user.image,
                },
                "message": data
            }
            await manager.broadcast_json(room_id, message)
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
