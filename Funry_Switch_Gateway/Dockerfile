# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN \
  apk add --no-cache \
    python3 \
    py3-pip
    
FROM python:3    

COPY rootfs /

RUN pip3 install -r requirements.txt

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
