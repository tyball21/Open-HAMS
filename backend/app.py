from fastapi import FastAPI

from api import users_router
from core.config import settings

app = FastAPI(title=settings.app_name, version=settings.app_version)


@app.get("/")
def hello():
    return {"Hello": "World"}


app.include_router(users_router)
