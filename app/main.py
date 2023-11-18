from fastapi import FastAPI
from routers import users

import os


app = FastAPI()

app.include_router(users.router)

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