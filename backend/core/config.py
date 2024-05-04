import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
print(os.getenv("DB_URI"))


class Config(BaseModel):
    app_name: str = "Open HAMS"
    app_description: str = "Open Source Habitat Animal Management System - A SaaS dashboard for Zoo's and ambassador programs for animal and event management. Designed for any organization to host and run their own animal management dashboard."
    app_version: str = "0.1.0"

    db_uri: str = os.getenv("DB_URI")


config = Config()
