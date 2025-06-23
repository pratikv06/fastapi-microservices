# stdlib
import json
from typing import Any

# third party
from dotenv import load_dotenv
from pydantic_settings import BaseSettings  # type: ignore


class Settings(BaseSettings):
    APP_DETAILS: dict[str, Any] = {}
    DEBUG: bool

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

    def __init__(self):
        load_dotenv()
        super().__init__()
        self.APP_DETAILS = self.load_tag_metadata()  # type: ignore

    def load_tag_metadata(self):
        print("Loading app details...")
        with open("src/app_details.json", "r") as file:
            return json.load(file)


settings = Settings()
