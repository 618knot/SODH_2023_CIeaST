"""
create_demo_users_table
"""
from sqlite3 import Connection, Cursor
from util.sqlite_util import *

conn: Connection = generate_connect()
cursor: Cursor = conn.cursor()

sql = create_table_sql(
    table_name="ademo_users",
    columns="""
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
    """)

cursor.execute(sql)
conn.commit()
conn.close()

print("created_demo_users_table")