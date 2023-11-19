from fastapi import APIRouter,WebSocket
from .util.sqlite_util import *
from fastapi.responses import HTMLResponse
import datetime

RESOURCE_NAME: str = "chat_rooms"
RESOURCE_COLUMNS: list = ["id", "tenant_id", "owner_id", "parking_id"]

router = APIRouter(
    prefix=f"/{RESOURCE_NAME}",
    tags=[RESOURCE_NAME]
)

# テスト用のHTML
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
            ws.onmessage = function(event) { //エンドポイントからのsendを受信する関数
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) { //エンドポイントに情報を送信する関数
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
    sql: str = "select * from chat_rooms where tenant_id = ? and owner_id = ? and parking_id = ?;"
    room: list = execute_query(sql, [tenant_id, owner_id, parking_id])
    return room

# チャットルームの作成
#TODO: postで確認してからroom_idでリダイレクト?
@router.post("/")
def create_chat_room(tenant_id: int,owner_id: int,parking_id: int) -> dict:
    # TODO: 駐車場の情報をもらう形式
    # TODO: ログインしているユーザIDをクッキーから取得
    print(select_chat_room(tenant_id, owner_id, parking_id))
    if not select_chat_room(tenant_id, owner_id, parking_id): # チャットルームが存在していなければ新しく作成
        sql: str = "insert into chat_rooms (tenant_id, owner_id, parking_id) values (?, ?, ?);"
        response = execute_update(sql, [tenant_id, owner_id, parking_id])
    else: # チャットルームが存在していれば存在していることを返す
        response = { "status": "ok", "message": "chat_room already exists" }
    return response

# チャットルームの取得
# URLにパラメータがあると勝手に知らん人のチャットに行ける脆弱性
@router.get("/")
def get_chat_room(room_id: int):
    # チャットルームに紐づけられたメッセージを取得
    sql: str = "select * from chat_messages where room_id = ?;"
    messages: list = execute_query(sql, (room_id,))

    # 既読をつける処理
    # TODO: ログインしているユーザIDをクッキーから取得
    user_id = 1 # 仮
    sql: str = "update chat_messages set is_read = ? where not speaker = ?;"
    response = execute_update(sql,[1, get_user_name(user_id)])

    # TODO: メッセージを返す形式
    return messages

def get_user_name(user_id: int):
    sql: str = "select name from users where id = ?"
    user_name: str = execute_query(sql, (user_id,))
    return user_name

def save_message(user_id: int,message: str) -> dict:
    sql: str = "insert into chat_messages (speaker, message, time, is_read, room_id) values (?, ?, ?, ?, ?);"
    now = datetime.datetime.now()
    response = execute_update(sql,[get_user_name(user_id), message, now, 0, RESOURCE_COLUMNS[0]])
    return response

@router.websocket("/end_point")
async def websocket_endpoint(ws: WebSocket):
    # TODO: 送信したユーザのIDを取得
    user_id = 1 #仮
    await ws.accept()
    while True:
        message = await ws.receive_text()
        await ws.send_text(f"{get_user_name(user_id)}:{message}")
        response = await save_message(user_id, message)
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
