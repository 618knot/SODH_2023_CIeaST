"""
create_sessions_table
"""
from sqlite3 import Connection, Cursor
from util.sqlite_util import *

conn: Connection = generate_connect()
cursor: Cursor = conn.cursor()

# 現段階ではsessionの有効期限は考慮しない
sql = create_table_sql(
    table_name="sessions",
    columns="""
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id)
    """)

cursor.execute(sql)
conn.commit()
conn.close()

print("created_sessions_table")