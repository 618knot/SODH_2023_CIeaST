from fastapi import FastAPI
from routers import users, sessions, web_socket_test
from starlette.middleware.cors import CORSMiddleware

import os


app = FastAPI()

# CORSを回避するために追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)
# ssl検証を無効にする
os.environ['UVICORN_CMD_SSL'] = '0'

# マイグレーションもどきをする(あんまりやりたくない)
@app.on_event("startup")
def startup_event() -> None:
    directory_path = 'migrations'
    for filename in os.listdir(directory_path):
        if filename.endswith('.py'):
            script_path = os.path.join(directory_path, filename)
            os.system(f'python {script_path}')

@app.get("/")
async def hello() -> str:
    return "HELLO"

app.include_router(users.router)
app.include_router(sessions.router)
app.include_router(web_socket_test.router)