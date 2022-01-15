FROM python:3.10.1-slim-bullseye

RUN apt-get update && apt-get install -y gcc
RUN apt-get -y install cron

RUN mkdir /app
RUN mkdir /app/lib
RUN mkdir /app/services
RUN mkdir /app/scraper

WORKDIR /app
ADD src/python/scraper /app/scraper
ADD src/python/services /app/services
ADD src/python/config.py /app/
ADD requirements.txt /app/

RUN pip install -r requirements.txt -t /app/lib


RUN touch /var/log/cron.log
RUN chmod +x /app/scraper/run_scraper
RUN (echo "* 2 * * * /app/scraper/run_scraper >> /var/log/cron.log") >> /etc/cron.d/root
RUN chmod 0644 /etc/cron.d/root
RUN crontab /etc/cron.d/root

ENV APP_PORT=8000
ENV PYTHONPATH="/app/lib:/app"
ENV OAUTHLIB_INSECURE_TRANSPORT=1

EXPOSE $APP_PORT
CMD ( cron -f -l 8 & )
CMD ["python", "/app/scraper/__init__.py"]
