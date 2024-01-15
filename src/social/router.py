from fastapi import APIRouter, Depends
from fastapi import WebSocket, WebSocketDisconnect
from typing_extensions import Annotated

from src.dependencies import get_current_user_ws
from src.social import models as social_models
from src.social.dependencies import valid_room_get
from src.social.exceptions import PermissionDeniedWS
from src.social.manager import ConnectionManager
from src.users import models as user_model

router = APIRouter()
manager = ConnectionManager()


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket,
                             room: Annotated[social_models.Room, Depends(valid_room_get)],
                             user: Annotated[user_model.User, Depends(get_current_user_ws)]):
    if user.room != room:
        raise PermissionDeniedWS
    await manager.connect(websocket)
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
            await manager.broadcast_json(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
