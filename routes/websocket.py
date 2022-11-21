from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import modules.mysql  as sql
import modules.other as tool
import json

app = FastAPI()
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <label>Target ID: <input type="text" id="targetID" autocomplete="off" value="001"/></label>
        <label>Group ID: <input type="text" id="groupID" autocomplete="off" value="001"/></label>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var groud_id = document.getElementById("groupID").value
            var ws = new WebSocket(`ws://chat.lovesusu.tw/ws/${client_id}/${groud_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                var targetID = document.getElementById("targetID")
                ws.send(JSON.stringify({
                    targetID: targetID.value,
                    data: input.value
                }))
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

class chat:
#   get chat_group where user_id
    @classmethod
    def getChatGroups(cls, user_id, target_id=None):
#       if target_id == None search public
        if target_id == None:
            res = sql.query.searchQuery('chat_group',{
                'user_id': '={}'.format(user_id),
                'group_status': '=0'
            })
        else:
            query =  "select * from chat_group \
                        where group_status='1' \
                        and user_id='{}' \
                        and group_id = (select group_id from chat_group where user_id ='{}') limit 1;".format(user_id, target_id)
            res = sql.query.query('chat_group', query)
        return res

    @classmethod
    def createChatGroups(cls, group_id, user_id):
            sql.query.update('chat_group', {
                'group_token': tool.hash.randomToken(),
                'group_id': group_id,
                'user_id': user_id
            })

    @classmethod
    def getChatGroupMember(cls, group_id):
        res = sql.query.searchQuery('chat_group',{
            'group_token': '={}'.format(group_token)
        })
        return res

    @classmethod
    async def getChatMessage(cls, group_id):
        res = sql.query.searchQuery('chat_message',{
            'group_id': '={}'.format(group_id)
        })
        return res

    @classmethod
    async def addChatMessage(cls, group_id, user_id, chat_content):
        sql.query.update('chat_message',{
            'chat_token': tool.hash.randomToken(),
            'group_id': group_id,
            'user_id': user_id,
            'chat_content': chat_content
        })

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[(WebSocket, str)] = []

    async def connect(self, websocket: WebSocket, user_id: str, group_id: str):
        await websocket.accept()
        self.active_connections.append((websocket, user_id))
#       when connect to websocket
#       get old chat message
        res = await chat.getChatMessage(group_id)
        await websocket.send_json(json.dumps({'data': res}, default=str))

    def disconnect(self, websocket: WebSocket, user_id: str):
        self.active_connections.remove((websocket, user_id))

#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection[0].send_text(message)

    async def send_private_message(self, message: str, user_id: str):
        for connection in self.active_connections:
            if connection[1] == user_id:
                await connection[0].send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)

@app.get("/chatCheck")
async def chatCheck(user_id: str = '001', target_id: str = '00'):

    res = chat.getChatGroups(user_id, target_id)

    return json.dumps({'data': res}, default=str)

@app.websocket("/ws/{user_id}/{group_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, group_id: str):
    await manager.connect(websocket, user_id, group_id)
    try:
        while True:
            data = await websocket.receive_json()
#           record to mysql
            await chat.addChatMessage(group_id, user_id, data['data'])
#           send bordcast to custom
            await manager.send_private_message(f"客戶 #{user_id} says: {data['data']}", data['targetID'])
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
#         await manager.broadcast(f"Client #{client_id} left the chat")
