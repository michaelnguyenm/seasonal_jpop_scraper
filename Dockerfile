FROM ubuntu:16.04

WORKDIR /home/app

ADD . /home/app

RUN apt-get -qq update && apt-get install -qq -y \
    python3 \
    python-pip

RUN pip install --upgrade pip && pip install -r requirements.txt
