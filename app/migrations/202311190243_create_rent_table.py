from sqlite3 import Connection, Cursor
from util.sqlite_util import *

conn: Connection = generate_connect()
cursor: Cursor = conn.cursor()

# 駐車場の登録テーブル作成
sql = create_table_sql(
    table_name="rent_parking",
    columns="""
    parking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_date TEXT NOT NULL,
    fee INTEGER NOT NULL,
    comment TEXT,
    address TEXT PRIMARY KEY NOT NULL,
    """)

cursor.execute(sql)
conn.commit()
conn.close()

print("created_rent_parking_table")
