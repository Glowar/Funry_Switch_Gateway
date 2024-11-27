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
RUN chmod a+x /src/main.py
#RUN chmod a+x /etc/services.d/funry_switch_gateway/run
#RUN chmod a+x /etc/services.d/funry_switch_gateway/finish
WORKDIR /src
RUN pip3 install -r requirements.txt
WORKDIR /
CMD python /src/main.py
