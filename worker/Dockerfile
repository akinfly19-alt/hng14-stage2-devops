# syntax=docker/dockerfile:1
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
# hadolint ignore=DL3013
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt --target /app/deps


FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app/deps /app/deps
ENV PYTHONPATH=/app/deps

COPY worker.py .

RUN adduser --disabled-password --gecos "" --uid 1001 appuser
USER appuser

HEALTHCHECK --interval=15s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import redis, os; r=redis.Redis(host=os.environ.get('REDIS_HOST','redis'), password=os.environ.get('REDIS_PASSWORD',None)); r.ping()" || exit 1

CMD ["python", "worker.py"]
