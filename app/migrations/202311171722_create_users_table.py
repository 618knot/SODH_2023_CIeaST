"""
create_users_table
"""
from sqlite3 import Connection, Cursor
from util.sqlite_util import *

conn: Connection = generate_connect()
cursor: Cursor = conn.cursor()

# 本当はパスワードをそのまま保存するのはマズい
sql = create_table_sql(
    table_name="users",
    columns="""
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
    """)

cursor.execute(sql)
conn.commit()
conn.close()

print("created_users_table")