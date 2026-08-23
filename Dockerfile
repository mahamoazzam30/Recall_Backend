# syntax=docker/dockerfile:1

# --- Stage 1: dependencies -------------------------------------------------
FROM python:3.11-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/opt/venv/bin:$PATH"

RUN python -m venv /opt/venv

WORKDIR /build

# Install the dependency set against a stub package so that editing application
# code doesn't invalidate this (slow) layer. The stub itself is uninstalled
# again immediately; only the third-party dependencies stay in the venv.
COPY pyproject.toml ./
RUN mkdir app \
    && touch app/__init__.py \
    && pip install . \
    && pip uninstall -y recall-backend


# --- Stage 2: runtime ------------------------------------------------------
FROM python:3.11-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH"

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

COPY alembic.ini ./
COPY alembic ./alembic
COPY app ./app
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

# Strip CRLF in case the script was checked out on Windows — a \r in the
# shebang line makes the container fail to start with a cryptic "not found".
RUN sed -i 's/\r$//' /usr/local/bin/docker-entrypoint.sh \
    && chmod +x /usr/local/bin/docker-entrypoint.sh

# app/llm/prompt_log.py appends to prompts.md on every LLM call, so the file
# has to exist and be writable by the unprivileged runtime user.
RUN useradd --create-home --uid 1000 recall \
    && touch prompts.md \
    && chown -R recall:recall /app
USER recall

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
