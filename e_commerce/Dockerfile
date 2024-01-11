# Dockerfile
FROM python:3.11-alpine

RUN pip install --upgrade pip

WORKDIR /e_commerce
COPY . /e_commerce

RUN pip install -r requirements.txt
