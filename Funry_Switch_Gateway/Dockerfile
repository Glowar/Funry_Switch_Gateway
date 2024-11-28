# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN \
  apk add --no-cache \
    python3
    
RUN pip install asyncio nest-asyncio pyserial-asyncio paho-mqtt
  
# Copy root filesystem 
COPY rootfs /

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
