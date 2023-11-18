from sqlite3 import Connection, Cursor
from util.sqlite_util import *

conn: Connection = generate_connect()
cursor: Cursor = conn.cursor()

# 駐車場の登録テーブル作成
sql = create_table_sql(
    table_name="apply_parking",
    columns="""
    parking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rent_name TEXT NOT NULL,
    address TEXT NOT NULL,
    fee INTEGER,
    comment TEXT,
    rent_term text NOT NULL,
    """)

cursor.execute(sql)
conn.commit()
conn.close()

print("created_apply_parking_table")
