from python:3.7

RUN apt-get update && apt-get install -y \
    python3-pip

RUN pip3 install --upgrade pip

RUN mkdir /app

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt



