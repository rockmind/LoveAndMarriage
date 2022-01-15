FROM python:3.10.1-slim-bullseye

RUN apt-get update && apt-get install -y gcc

RUN mkdir /app
RUN mkdir /app/lib
RUN mkdir /app/services

WORKDIR /app

ADD src/python/services /app/services
ADD src/python/config.py /app/
ADD requirements.txt /app/

RUN pip install -r requirements.txt -t /app/lib

