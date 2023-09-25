# syntax=docker/dockerfile:1

FROM python:3.10.2-slim-buster
RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FASTAPI_RUN_PORT=80
ENV FASTAPI_RUN_HOST=0.0.0.0

EXPOSE 80

CMD ["gunicorn"  , "--bind", "0.0.0.0:80", "app:app"]