import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

DOTENV = os.path.join(os.path.dirname(__file__), '.env')

class Settings(BaseSettings):
    DATABASE_URL: str = Field(default="", description="Database URL")

    model_config = SettingsConfigDict(env_file=DOTENV)

settings = Settings()

