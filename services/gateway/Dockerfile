FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY app/ .
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["uv", "run", "python", "-m", "app.main"]
# CMD ["uv", "run", "uvicorn", "app:main:app"]
