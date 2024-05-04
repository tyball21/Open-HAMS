import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Config(BaseModel):
    db_uri: str = os.getenv("DB_URI")


config = Config()
