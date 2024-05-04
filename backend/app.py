from fastapi import FastAPI

from api import users_router
from core.config import config

app = FastAPI(title=config.app_name, version=config.app_version)


@app.get("/")
def hello():
    return {"Hello": "World"}


app.include_router(users_router)
