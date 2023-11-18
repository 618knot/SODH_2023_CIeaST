"""
申請
"""

from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

from .util.sqlite_util import *

RESOURCE_NAME: str = "apply_parking"
RESOURCE_COLUMNS: list = ["parking_id", "rent_name", "address", "fee", "comment", "rent_term"]

router: APIRouter = APIRouter(
    prefix=f"/{RESOURCE_NAME}",
    tags=[RESOURCE_NAME],
)

class UserProp(BaseModel):
    rent_name: str
    address: str
    fee: int
    comment: str
    rent_term: str

@router.post("/{id}/apply/{parking_id}")
async def create(props: UserProp):
    # TODO: 空文字を入力された時の対策
    sql: str = "insert into parking_spaces (rent_term) values (?);"
    response = execute_update(sql, [(props.rent_term)])

    return response

@router.get("/{id}/apply/{parking_id}")
async def applyGet(parking_id: int):
    try:
        sql: str = f"select parking_id, start_date, address, fee, comment from rent where parking_id = ?;"
        result: list = execute_query(sql, (parking_id,))

        return { "status": "ok" } if len(result) != 0 else { "status": "not ok" }
    except:
        return { "status": "not ok" }