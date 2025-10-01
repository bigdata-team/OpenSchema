FROM python:3.12-slim AS installer

ARG SERVICE_NAME

WORKDIR /app

RUN pip install --upgrade pip
COPY service/${SERVICE_NAME}/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM installer

ARG SERVICE_NAME

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y curl && apt-get clean

COPY service/${SERVICE_NAME} ./
COPY common ./common

EXPOSE 8000

# CMD [ "fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD uvicorn ${SERVICE_NAME}.main:app --host 0.0.0.0 --port 8000
