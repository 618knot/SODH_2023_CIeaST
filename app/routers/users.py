"""
ユーザー
"""

from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

from .util.sqlite_util import *

RESOURCE_NAME: str = "users"
RESOURCE_COLUMNS: list = ["id", "name", "email", "password"]

router: APIRouter = APIRouter(
    prefix=f"/{RESOURCE_NAME}",
    tags=[RESOURCE_NAME],
)

class UserProp(BaseModel):
    name: str
    email: str
    password: str

@router.post("/register")
async def create(props: UserProp):
    # TODO: 空文字を入力された時の対策
    sql: str = "insert into users (name, email, password) values (?, ?, ?);"
    response = execute_update(sql, [(props.name, props.email, props.password)])

    return response

#オーナーが通知を取得
@router.post("/chat_notice")
async def notice():
    # 自分がオーナーのチャットルームのidを取得
    sql: str = "select id from chat_rooms where owner_id = ?"
    room_ids: list = execute_query(sql, (RESOURCE_COLUMNS[0],))

    if not room_ids:
        return { "status": "ok", "notices": 0 }

    sql: str = "select id from chat_messages where room_id = ? and is_read = ?"
    notice_count = 0
    for room_id in room_ids:
        notices: list = execute_query(sql, [room_id[0], 0])
        notice_count += notices.count()

    return { "status": "ok", "notices": {notice_count} }

