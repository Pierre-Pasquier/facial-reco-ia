FROM ubuntu:22.04

RUN apt-get update \
&& apt-get install -y python3 \
&& apt-get install -y python3-pip \
&& pip install --upgrade pip

ADD . /facial-reco-ia/
WORKDIR /facial-reco-ia

VOLUME /facial-reco-ia