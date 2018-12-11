FROM debian:buster

RUN apt-get update \
    && apt-get upgrade -y 

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends apt-utils

RUN apt-get install -y autotools-dev \
  && apt-get install -y make \
  && apt-get install -y gcc \
  && apt-get install -y libtool \
  && apt install -y g++


RUN mkdir -p /home/deb
WORKDIR /home/deb

ADD . .
RUN chmod +x install.sh
