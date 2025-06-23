# stdlib
import json
from typing import Any

# third party
from dotenv import load_dotenv
from pydantic_settings import BaseSettings  # type: ignore


class Settings(BaseSettings):
    APP_DETAILS: dict[str, Any]
    DEBUG: bool

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_SERVER: str
    DB_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    EMAIL_OTP_SERVICE: str
    PASSWORD_OTP_SERVICE: str

    ECHO_SQL: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

    def __init__(self):
        load_dotenv()
        super().__init__()
        self.APP_DETAILS = self.load_tag_metadata()  # type: ignore

    def load_tag_metadata(self):
        with open("app_details.json", "r") as file:
            return json.load(file)

    @property
    def POSTGRES_DB_URL(self) -> str:
        """Returns the database URL"""
        return (
            f"postgresql+asyncpg://"
            f"{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@"
            f"{self.DB_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )


settings = Settings()
