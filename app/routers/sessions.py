"""
セッション(ログイン管理)
"""

from fastapi import APIRouter
from pydantic import BaseModel

from .util.sqlite_util import *

RESOURCE_NAME: str = "sessions"
RESOURCE_COLUMNS: list = ["id", "user_id"]

router: APIRouter = APIRouter(
    prefix=f"/{RESOURCE_NAME}",
    tags=[RESOURCE_NAME],
)

class LoginProp(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(props: LoginProp):
    try:
        sql: str = "select id from users where email = ?and password = ?;"
        result: list = execute_query(sql, (props.email, props.password))
        user_id = result[0]

    except:
        return { "status": "error", "message": "ユーザーが登録されていません" }
    
    try:
        sql: str = "insert into sessions (user_id) values (?);"
        update_successed = execute_update(sql, [user_id,]) # execute_updateが値を返すように改修したため

        sql: str = "select id from sessions where user_id = (?);"
        session_id = execute_query(sql, user_id)[0][0]
        return { "status": "ok", "session id": session_id }
    except:
        return { "status": "error", "message": "エラーが発生しました" }

@router.get("/{id}")
async def isLogin(id: int):
    try:
        sql: str = f"select id from sessions where user_id = ?;"
        result: list = execute_query(sql, (id,))

        return { "status": "logged in" } if len(result) != 0 else { "status": "not logged in" }
    except:
        return { "status": "not logged in" }
