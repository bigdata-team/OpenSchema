FROM python:3.12-slim AS installer

ARG SERVICE_DIR

WORKDIR /app

RUN pip install --upgrade pip
COPY src/service/${SERVICE_DIR}/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

FROM installer

ARG SERVICE_DIR

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y curl && apt-get clean

COPY src/service/${SERVICE_DIR} ./
COPY src/common ./common

EXPOSE 8000

# CMD [ "fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD uvicorn ${SERVICE_DIR}.main:app --host 0.0.0.0 --port 8000
