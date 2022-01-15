FROM base-container:latest

RUN mkdir /app/covid_db_api

WORKDIR /app
ADD src/python/covid_db_api /app/covid_db_api
ADD src/python/services /app/services
ADD src/python/config.py /app/

ENV APP_PORT=8000
ENV PYTHONPATH="/app/lib:/app"

EXPOSE $APP_PORT
CMD ["python", "/app/covid_db_api/__init__.py"]
