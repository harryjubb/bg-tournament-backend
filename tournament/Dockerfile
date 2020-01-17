FROM python:3.8.1
LABEL maintainer="harry.jubb@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app/
