import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from api_rest_mini_blog.database import Base
from api_rest_mini_blog.database import get_db as get_async_session
from tests.utils_db import recreate_test_database, run_migrations, delete_test_database
from api_rest_mini_blog.config import settings

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    recreate_test_database()
    run_migrations()
    yield
    delete_test_database()

@pytest_asyncio.fixture(scope="function")
async def db_session():
    engine = create_async_engine(settings.TEST_DATABASE_URL, future=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)
    async with async_session() as session:
        yield session
    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session):
    from api_rest_mini_blog.main import app

    async def override_get_async_session():
        yield db_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
