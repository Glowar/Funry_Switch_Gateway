# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

ENV PYTHONUNBUFFERED=1

COPY rootfs /
RUN chmod a+x /src/*
RUN chmod a+x /etc/*

WORKDIR /src

RUN pip3 install -r requirements.txt

WORKDIR /
