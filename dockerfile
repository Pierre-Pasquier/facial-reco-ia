FROM ubuntu:22.04

ADD . /facial-reco-ia/
WORKDIR /facial-reco-ia

RUN apt-get update \
&& apt-get install -y python3 \
&& apt-get install -y python3-pip \
&& pip install --upgrade pip

RUN pip install -r requirements.txt

VOLUME /facial-reco-ia