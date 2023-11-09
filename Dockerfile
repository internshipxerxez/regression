FROM python:3.8-slim

LABEL maintainer="xerxez.in"

ENV PYTHONNUNBUFFERED 1

COPY ./requirements_docker.txt /requiremnets_docker.txt
COPY ./webapp /webapp
COPY ./models/model.joblib /models/model.joblib

WORKDIR /webapp

EXPOSE 8000

RUN python -m venv /py

RUN /py/bin/pip install -r /requiremnets_docker.txt

RUN /py/bin/pip install --upgrade pip
RUN python -m pip install --upgrade pip

#RUN apk add --update --no-cache --virtual linux-headers
#RUN adduser --disable-password --no-create-home webapp

ENV PATH="/py/bin:$PATH"

#USER app

#USER webapp
