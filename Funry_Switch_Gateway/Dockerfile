# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN \
  apk add --no-cache \
    python3 \
    py3-pip
    
RUN \
  pip3 install asyncio && \
  pip3 install nest-asyncio && \
  pip3 install pyserial-asyncio && \
  pip3 install paho-mqtt
  
# Copy root filesystem 
COPY rootfs /

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
