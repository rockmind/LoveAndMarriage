FROM base-container:latest

RUN mkdir /app/front

WORKDIR /app
ADD src/python/front /app/front
ADD src/python/services /app/services
ADD src/python/config.py /app/

ENV APP_PORT=8000
ENV PYTHONPATH="/app/lib:/app"
ENV OAUTHLIB_INSECURE_TRANSPORT=1

EXPOSE $APP_PORT
CMD ["python", "/app/front/__init__.py"]
