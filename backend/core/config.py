import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Config(BaseModel):
    APP_NAME: str = "Open HAMS"
    APP_DESC: str = "Open Source Habitat Animal Management System - A SaaS dashboard for Zoo's and ambassador programs for animal and event management. Designed for any organization to host and run their own animal management dashboard."
    APP_VERSION: str = "0.1.0"

    DB_URI: str = os.getenv("DB_URI")
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    # Admin User
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD")
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL")
    

settings = Config()
