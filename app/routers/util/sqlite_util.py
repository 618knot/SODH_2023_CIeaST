"""
SQLiteの汎用処理
"""

from sqlite3 import connect, Cursor, Connection
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)
DOTENV_PATH: str = join(dirname(__file__), '.env')
load_dotenv(DOTENV_PATH)

DB_NAME: str = os.environ.get("DB_NAME")

def generate_connect() -> Cursor:
    return connect(DB_NAME)

def create_table_sql(table_name: str, columns: str) -> str:
    sql = """
    CREATE TABLE IF NOT EXISTS {0} (
        {1}
    );
    """.format(table_name, columns)

    return sql

def execute_query(sql: str) -> list:
    conn: Connection = generate_connect()
    cursor: Cursor = conn.cursor()
    cursor.execute(sql)  # SQLクエリを実行
    result = cursor.fetchall()  # 結果を取得
    conn.close()  # 接続を閉じる
    return result

def execute_update(sql: str, data: list) -> None:
    conn: Connection = generate_connect()
    cursor: Cursor = conn.cursor()
    cursor.executemany(sql, data)  # 複数のレコードを処理
    conn.commit()  # 変更をコミット
    conn.close()  # 接続を閉じる
