FROM ubuntu:16.04

WORKDIR /home/app

ADD . /home/app

RUN apt-get -qq update && apt-get install -qq -y \
    python3 \
    python3-pip

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
