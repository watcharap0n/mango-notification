FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

LABEL maintainer="wera.watcharapon@gmail.com"
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY /server /app
WORKDIR /app

