from sqlalchemy.ext.asyncio import create_async_engine

from core.config import settings

engine = create_async_engine(settings.DB_URI, echo=True)
