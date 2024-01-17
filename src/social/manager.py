from typing import Dict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict = {}

    async def connect(self, room_id: int, websocket: WebSocket):
        await websocket.accept()
        if room_id in self.active_connections:
            self.active_connections[room_id].append(websocket)
        else:
            self.active_connections[room_id] = [websocket]

    def disconnect(self, room_id: int, websocket: WebSocket):
        self.active_connections[room_id].remove(websocket)

    async def broadcast_text(self, room_id: int, message: str):
        for connection in self.active_connections[room_id]:
            await connection.send_text(message)

    async def broadcast_json(self, room_id: int, message: dict):
        for connection in self.active_connections[room_id]:
            await connection.send_json(message)
