from contextlib import asynccontextmanager

from api import api_router
from api.seed import create_admin, seed_db
from core.config import settings
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_db()
    await create_admin()
    yield


app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, lifespan=lifespan)


app.include_router(api_router)

# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html_cdn():
#     return get_swagger_ui_html(
#     openapi_url=app.openapi_url,
#     title=f"{app.title} - Swagger UI",
#     swagger_css_url="https://cdn.jsdelivr.net/gh/Itz-fork/Fastapi-Swagger-UI-Dark/assets/swagger_ui_dark.min.css"
# )
