FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
# We are installing a dependency
ADD requirements.txt /app/requirements.txt
RUN apk add --no-cache g++ zlib-dev make && pip3 install -r /app/requirements.txt

ADD src/* /app/
ENV PYTHONPATH /app
ENTRYPOINT cd /app/ && python3 main.py