"""
ユーザー
"""

from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

from .util.sqlite_util import *

RESOURCE_NAME: str = "rent_parking"
RESOURCE_COLUMNS: list = ["parking_id", "start-date", "fee", "comment", "address"]

router: APIRouter = APIRouter(
    prefix=f"/{RESOURCE_NAME}",
    tags=[RESOURCE_NAME],
)

class UserProp(BaseModel):
    start_date: str
    fee: int
    comment: str
    address: str

@router.post("/{id}/rent/{parking_id}")
async def create(props: UserProp):
    # TODO: 空文字を入力された時の対策
    sql: str = "insert into parking_spaces (start_date, fee, comment, address) values (?, ?, ?, ?);"
    response = execute_update(sql, [(props.start_date, props.fee, props.comment, props.address)])

    return response
