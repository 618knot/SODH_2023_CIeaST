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
    sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {columns}
    );
    """

    return sql