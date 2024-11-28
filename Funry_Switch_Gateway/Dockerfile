# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache \
    python3 \
    py3-pip \
  && pip3 install paho-mqtt

WORKDIR ./

COPY src / 

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
