FROM python:3.6-slim

RUN apt-get update && apt-get -y install build-essential

RUN pip install flask redis kubernetes==10.0.0 gunicorn pandas influxdb

ADD app /app

WORKDIR /app
