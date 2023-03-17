FROM python:3.11.1-slim

WORKDIR /cap_bot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt bot.py /cap_bot/

COPY bot /cap_bot/bot/
COPY utils /cap_bot/utils/
COPY providers /cap_bot/providers/

RUN pip install --no-cache-dir --upgrade -r requirements.txt
