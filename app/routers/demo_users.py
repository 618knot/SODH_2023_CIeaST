"""
実験用
"""

from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

from sqlite3 import Connection, Cursor
from .util.sqlite_util import *

RESOURCE_NAME: str = "demo_users"
RESOURCE_COLUMNS: list = ["id", "name", "email"]

router: APIRouter = APIRouter(
    prefix=f"/{RESOURCE_NAME}",
    tags=[RESOURCE_NAME],
)

class DemoUserProp(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

# なんか起動時にやりたいときはon_eventで書く
@router.on_event("startup")
async def startup_event() -> None:
    pass

@router.get("/")
async def show() -> dict:
    conn: Connection = generate_connect()
    cursor: Cursor = conn.cursor()

    sql: str ="select * from demo_users;"
    cursor.execute(sql)
    items: list = cursor.fetchall()

    cursor.close()
    conn.close()

    response: dict = {}
    for item in items:
        response[item[0]] = { RESOURCE_COLUMNS[1]: item[1], RESOURCE_COLUMNS[2]: item[2] }
    
    return response

@router.post("/")
async def create(prop: DemoUserProp) -> dict:
    conn: Connection = generate_connect()
    cursor: Cursor = conn.cursor()

    sql: str = "insert into demo_users (name, email) values (?, ?);"
    cursor.execute(sql, (prop.name, prop.email))

    conn.commit()
    conn.close()

    return { "status": "ok" }

@router.put("/{id}")
async def update(id: int, prop: DemoUserProp) -> dict:
    conn: Connection = generate_connect()
    cursor: Cursor = conn.cursor()

    sql: str = "update demo_users set name = ? where id = ?"
    cursor.execute(sql, (prop.name, id))

    conn.commit()
    conn.close()

    return { "status": "ok" }

@router.delete("/{id}")
async def destroy(id: int) -> dict:
    conn: Connection = generate_connect()
    cursor: Cursor = conn.cursor()

    sql: str = "delete from demo_users where id = ?"
    cursor.execute(sql, (id,))

    conn.commit()
    conn.close()

    return { "status": "ok" }
