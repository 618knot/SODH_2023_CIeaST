"""
登録
"""

from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

from .util.sqlite_util import *

RESOURCE_NAME: str = "rent_parking"
RESOURCE_COLUMNS: list = ["parking_id", "rent_user_name", "start-date", "fee", "comment", "address"]

router: APIRouter = APIRouter(
    prefix=f"/{RESOURCE_NAME}",
    tags=[RESOURCE_NAME],
)

class ParkingProps(BaseModel):
    start_date: str
    fee: int
    comment: str
    address: str

@router.post("/{session_id}")
async def create(props: ParkingProps, session_id: int):
    sql: str = "select user_id from sessions where id = ?;"
    result: list = execute_query(sql, (session_id,))

    sql: str = "select name from users where id = ?;"
    result: list = execute_query(sql, (result[0][0],))
    rent_user_name = result[0][0]
    print(rent_user_name)

    # TODO: 空文字を入力された時の対策
    sql: str = "insert into rent_parking (rent_user_name, start_date, fee, comment, address) values (?, ?, ?, ?, ?);"
    response = execute_update(sql, [(rent_user_name, props.start_date, props.fee, props.comment, props.address)])

    return response
