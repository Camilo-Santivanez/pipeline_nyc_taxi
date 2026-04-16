#Usar una version específica 
FROM python:3.13.11-slim

#Instalar UV de forma eficiente
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY pyproject.toml .python-version uv.lock ./

RUN uv sync --locked

COPY nyc_taxi_data.py .

ENTRYPOINT ["python", "nyc_taxi_data.py"]
