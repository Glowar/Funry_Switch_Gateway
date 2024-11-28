# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile

FROM python:3

COPY src /src

WORKDIR /etc/

RUN \
  pip3 install asyncio && \
  pip3 install nest-asyncio && \
  pip3 install pyserial-asyncio && \
  pip3 install paho-mqtt

WORKDIR /src

RUN chmod a+x run.sh
CMD [ "/run.sh" ]
