from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from pydantic import BaseModel
from routes.member import get_current_active_user
from modules.TOOLS import dict_protect_sql
import json
router = APIRouter()




class ConnectionManager:
    
    def __init__(self):
        self.active_connections: List[(WebSocket, str)] = []

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections.append((websocket, user_id))
#       when connect to websocket
#       get old chat message
#         res = await chat.getChatMessage(group_id)
        await websocket.send_json(json.dumps({"message": "大家好~歡迎加入本聊天室"}, default=str))

    def disconnect(self, websocket: WebSocket, user_id: str):
        self.active_connections.remove((websocket, user_id))

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection[0].send_text(message)

    async def send_private_message(self, data, user_id: str):
        data = dict_protect_sql(data)
        for connection in self.active_connections:
            if connection[1] == user_id:

                await connection[0].send_json(json.dumps(data, default=str))


manager = ConnectionManager()


@router.websocket("/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.send_private_message(data,data['receiver_id'])
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
