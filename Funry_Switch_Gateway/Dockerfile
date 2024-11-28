# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

FROM python:3

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir paho-mqtt
    
# Copy root filesystem 
COPY src / 

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
