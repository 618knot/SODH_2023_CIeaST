from fastapi import APIRouter,WebSocket
from .util.sqlite_util import *
from fastapi.responses import HTMLResponse

RESOURCE_NAME: str = "chat_rooms"
RESOURCE_COLUMNS: list = ["id", "user_id"]

router = APIRouter(
    prefix=f"/{RESOURCE_NAME}",
    tags=[RESOURCE_NAME]
)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/end_point");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

def select_chat_room(tenant_id: int,owner_id: int,parking_id: int):
    sql: str = "select * from chat_rooms where tenant = ? and owner = ? and parking = ? limit 1;"
    room: list = execute_query(sql, [(tenant_id, owner_id, parking_id)])
    return room

#TODO: postで確認してからroom_idでリダイレクト?
@router.get("/")
def create_chat_room(tenant_id: int,owner_id: int,parking_id: int):
    # TODO: 駐車場の情報をもらう形式
    # TODO: ログインしているユーザIDをクッキーから取得
    # チャットルームが存在しているか確認
    room = select_chat_room(tenant_id, owner_id, parking_id)
    if not room: # 存在していなければ新しくチャットルームを作成
        sql: str = "insert into chat_rooms (tenant, owner, parking) values (?, ?, ?);"
        execute_update(sql, [(tenant_id, owner_id, parking_id)])
        response = execute_update(sql, [(tenant_id, owner_id, parking_id)])
        # TODO: チャットルームを返す形式
        return select_chat_room(tenant_id, owner_id, parking_id) #仮
    else: # 存在していればそのチャットルームを返す
        # TODO: チャットルームを返す形式
        return room # 仮
    # テスト用
    # return HTMLResponse(html)

# 各チャットルームの取得
# URLにパラメータがあると勝手に知らん人のチャットに行ける脆弱性
@router.get("/{id}")
def get_chat_room(room_id: int):
    # チャットルームに紐づけられたメッセージを取得
    sql: str = "select * from chat_messages where chat_rooms = ?;"
    messages: list = execute_query(sql, room_id)
    # TODO: メッセージを返す形式
    return messages

@router.websocket("/end_point")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_text()
        await ws.send_text(f"Message text was: {data}")
    # await ws.accept()
    # # クライアントを識別するためのIDを取得
    # key = ws.headers.get('sec-websocket-key')
    # clients[key] = ws
    # try:
    #     while True:
    #         # クライアントからメッセージを受信
    #         data = await ws.receive_text()
    #         # 接続中のクライアントそれぞれにメッセージを送信（ブロードキャスト）
    #         for client in clients.values():
    #             await client.send_text(f"ID: {key} | Message: {data}")
    # except:
    #     await ws.close()
    #     # 接続が切れた場合、当該クライアントを削除する
    #     del clients[key]
    #
    # return response