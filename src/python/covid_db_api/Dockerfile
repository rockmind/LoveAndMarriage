FROM python:3.10.1-slim-bullseye

RUN mkdir /app
RUN mkdir /app/lib
RUN mkdir /app/services
RUN mkdir /app/covid_db_api

WORKDIR /app
ADD src/python/covid_db_api /app/covid_db_api
ADD src/python/services /app/services
ADD requirements.txt /app/
RUN apt-get update && apt-get install -y gcc
RUN pip install -r requirements.txt -t /app/lib


ENV APP_PORT=8000
ENV PYTHONPATH="/app/lib:/app"

EXPOSE $APP_PORT
CMD ["python", "/app/covid_db_api/__init__.py"]
