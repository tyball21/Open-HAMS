from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    APP_NAME: str = "Open HAMS"
    APP_DESC: str = "Open Source Habitat Animal Management System - A SaaS dashboard for Zoo's and ambassador programs for animal and event management. Designed for any organization to host and run their own animal management dashboard."
    APP_VERSION: str = "0.1.0"

    DB_URI: str
    SECRET_KEY: str

    # Admin User
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    ADMIN_EMAIL: str

    # Main Zoo Info
    ZOO_NAME: str = "Utah's Hogle Zoo"
    ZOO_LOCATION: str = "Salt Lake City, UT"

    # AWS Credentials
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    AWS_BUCKET_NAME: str

    # RESEND API KEY
    RESEND_API_KEY: str


settings = Config()  # type: ignore
