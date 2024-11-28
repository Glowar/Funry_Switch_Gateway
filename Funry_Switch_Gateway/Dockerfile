# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN \
  apk add --no-cache \
    python3 \
	py3-pip

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir paho-mqtt

WORKDIR ./

COPY src / 

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
