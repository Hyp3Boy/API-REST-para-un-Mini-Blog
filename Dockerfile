FROM python:3.11-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root --no-dev --no-interaction --no-ansi


FROM python:3.11-slim as runtime

WORKDIR /app

RUN addgroup --system nonroot && adduser --system --group nonroot
USER nonroot

COPY --from=builder /app/.venv ./.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY ./src/api_rest_mini_blog ./src/api_rest_mini_blog
COPY ./alembic ./alembic
COPY alembic.ini .

EXPOSE 8000

CMD ["uvicorn", "src.api_rest_mini_blog.main:app", "--host", "0.0.0.0", "--port", "8000"]