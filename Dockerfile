FROM python:3.10.2-alpine3.15

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /src
COPY src/ /src/

WORKDIR /src
ENV PYTHONUNBUFFERED=1
