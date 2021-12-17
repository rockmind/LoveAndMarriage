FROM python:3.10.1-slim-bullseye

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN apt-get update && apt-get install -y gcc
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "/app/src/python/test_app/main.py"]
