# ── Build stage ──────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

COPY pyproject.toml README.md LICENSE ./
COPY admin_meta_agents/ admin_meta_agents/

RUN pip install --no-cache-dir --prefix=/install .

# ── Runtime stage ────────────────────────────────────────────────────
FROM python:3.12-slim

LABEL maintainer="JoshuaHCole"
LABEL description="Admin Meta-Agents orchestration framework"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Non-root user for security
RUN groupadd --gid 1000 app && \
    useradd --uid 1000 --gid app --create-home app

WORKDIR /app

COPY --from=builder /install /usr/local
COPY admin_meta_agents/ admin_meta_agents/
COPY main.py .

RUN chown -R app:app /app
USER app

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "from admin_meta_agents import MetaAgent; print('ok')" || exit 1

ENTRYPOINT ["python", "main.py"]
