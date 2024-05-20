from contextlib import asynccontextmanager

from api import api_router
from api.deps import SessionDep
from api.seed import create_admin, create_zoo, seed_db
from core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Permission, Role, RolePermission, User
from sqlmodel import select


@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_db()
    await create_zoo()
    await create_admin()
    yield


# Add cors

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # will be changed to the frontend url
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


# For debugging purposes
@app.get("/clear")
async def clear(session: SessionDep):
    async def truncate_table(model):
        objs = await session.exec(select(model))
        for obj in objs:
            await session.delete(obj)
        await session.commit()

    models = [User, RolePermission, Permission, Role]
    for model in models:
        await truncate_table(model)

    return {"message": "Tables cleared"}
