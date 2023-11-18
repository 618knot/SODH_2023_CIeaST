from sqlite3 import Connection, Cursor
from util.sqlite_util import *

conn: Connection = generate_connect()
cursor: Cursor = conn.cursor()

sql = create_table_sql(
    table_name="chat_rooms",
    columns="""
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    FOREIGN KEY (tenant_id) REFERENCES users (id),
    FOREIGN KEY (owner_id) REFERENCES users (id),
    parking_id INTEGER
    """)
# TODO: 駐車場テーブルが完成したらこれにする
# FOREIGN KEY (parking_id) REFERENCES #{駐車場のテーブル} (id)

cursor.execute(sql)
conn.commit()
conn.close()

print("created_chat_rooms_table")