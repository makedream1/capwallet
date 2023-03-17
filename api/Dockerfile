FROM python:3.11.1-slim

WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt main.py /api/

COPY api /api/api/
COPY utils /api/utils/
COPY providers /api/providers/
COPY images /api/images/

RUN pip install --no-cache-dir --upgrade -r requirements.txt
