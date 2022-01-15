FROM base-container:latest

RUN apt-get -y install cron

RUN mkdir /app/scraper

WORKDIR /app
ADD src/python/scraper /app/scraper
ADD src/python/services /app/services
ADD src/python/config.py /app/

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
