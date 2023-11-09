FROM ubuntu:22.04

RUN apt-get update \
&& apt-get install -y python3

ADD . /facial-reco-ia/
WORKDIR /facial-reco-ia

VOLUME /facial-reco-ia