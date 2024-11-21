# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

ENV PYTHONUNBUFFERED=1

COPY rootfs /

WORKDIR /src

RUN pip3 install -r requirements.txt

WORKDIR /
