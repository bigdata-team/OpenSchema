<<<<<<< HEAD
FROM python:3.12-slim AS installer

ARG SERVICE_NAME

WORKDIR /app

RUN pip install --upgrade pip
COPY service/${SERVICE_NAME}/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

FROM installer

ARG SERVICE_NAME
=======
FROM python:3.12-slim

ARG SERVICE_DIR
>>>>>>> 4a1a985 (add: v1.2)

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y curl && apt-get clean

<<<<<<< HEAD
COPY service/${SERVICE_NAME} ./
COPY common ./common

EXPOSE 8000

# CMD [ "fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD uvicorn ${SERVICE_NAME}.main:app --host 0.0.0.0 --port 8000
=======
COPY src/service/${SERVICE_DIR}/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/service/${SERVICE_DIR} ./
COPY src/common ./common

EXPOSE 8000

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]
>>>>>>> 4a1a985 (add: v1.2)
