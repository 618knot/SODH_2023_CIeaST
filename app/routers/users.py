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