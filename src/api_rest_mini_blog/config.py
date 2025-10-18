from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    ENVIRONMENT: str = Field(default="development", description="Environment type")
    DATABASE_URL: str = Field(default="", description="Database URL")
    TEST_DATABASE_URL: str = Field(default="", description="Test Database URL")
    postgres_user: str = Field(default="", description="Postgres user")
    postgres_password: str = Field(default="", description="Postgres password")
    postgres_db: str = Field(default="", description="Postgres database")
    postgres_host: str = Field(default="", description="Postgres host")

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()

