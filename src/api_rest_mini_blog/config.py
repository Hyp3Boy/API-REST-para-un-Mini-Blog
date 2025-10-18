from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    ENVIRONMENT: str = Field(default="development", description="Environment type")
    DATABASE_URL: str = Field(default="", description="Database URL")
    TEST_DATABASE_URL: str = Field(default="", description="Test Database URL")

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()

