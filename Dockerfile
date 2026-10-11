
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DEFAULT_TIMEOUT=300

COPY requirements.txt .

RUN pip install --no-cache-dir --timeout 300 \
    torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir --timeout 300 -r requirements.txt

RUN pip install --no-cache-dir --timeout 300 transformers sentence-transformers

COPY app.py .
COPY src/ ./src/
COPY templates/ ./templates/
COPY static/ ./static/

EXPOSE 10000

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-10000} app:app"]
