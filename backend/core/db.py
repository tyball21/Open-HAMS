from sqlalchemy.ext.asyncio import create_async_engine

from core.config import config

engine = create_async_engine(config.db_uri, echo=True)
