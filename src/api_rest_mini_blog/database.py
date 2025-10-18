from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from sqlalchemy.orm import declarative_base
from api_rest_mini_blog.config import settings

# Motor de base de datos asíncrono
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Fábrica de sesiones asíncronas
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base declarativa para los modelos
Base = declarative_base()

# Dependencia para obtener una sesión de base de datos
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session