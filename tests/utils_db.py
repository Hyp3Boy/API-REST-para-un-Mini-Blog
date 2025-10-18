import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from api_rest_mini_blog.config import settings
from urllib.parse import urlparse


def recreate_test_database():
    """Elimina y crea la BD de test desde postgres."""
    parsed = urlparse(settings.TEST_DATABASE_URL)
    db_name = parsed.path[1:]
    base_conn_str = f"dbname=postgres user={parsed.username} password={parsed.password} host={parsed.hostname} port={parsed.port}"

    conn = psycopg2.connect(base_conn_str)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{db_name}';")
    cur.execute(f"DROP DATABASE IF EXISTS {db_name};")
    cur.execute(f"CREATE DATABASE {db_name};")

    cur.close()
    conn.close()

def delete_test_database():
    """Elimina la BD de test desde postgres."""
    parsed = urlparse(settings.TEST_DATABASE_URL)
    db_name = parsed.path[1:]
    base_conn_str = f"dbname=postgres user={parsed.username} password={parsed.password} host={parsed.hostname} port={parsed.port}"

    conn = psycopg2.connect(base_conn_str)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{db_name}';")
    cur.execute(f"DROP DATABASE IF EXISTS {db_name};")

    cur.close()
    conn.close()


def run_migrations():
    """Ejecuta alembic upgrade head sobre la BD de test."""
    subprocess.run(["poetry", "run", "alembic", "upgrade", "head"], check=True)
