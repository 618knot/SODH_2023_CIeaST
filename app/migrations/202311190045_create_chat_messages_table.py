"""
create_chat_messages_table
"""
from sqlite3 import Connection, Cursor
from util.sqlite_util import *

conn: Connection = generate_connect()
cursor: Cursor = conn.cursor()

sql = create_table_sql(
    table_name="chat_messages",
    columns="""
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    speaker_id INTEGER,
    message TEXT,
    time TEXT,
    is_read INTEGER,
    FOREIGN KEY (room_id) REFERENCES chat_rooms (id)
    """)

cursor.execute(sql)
conn.commit()
conn.close()

print("created_chat_messages_table")