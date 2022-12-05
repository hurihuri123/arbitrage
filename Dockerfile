# syntax=docker/dockerfile:1
FROM python:3.6-slim

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install install vim

WORKDIR /app

COPY . .

RUN pip install python-kucoin python-binance
RUN cp exchanges/kucoin_source.py  /usr/local/lib/python3.6/site-packages/kucoin/client.py


CMD [ "python3", "-u" , "main.py"]