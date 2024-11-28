ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN \
  apk add --no-cache \
    python3 \
    bash \
    py3-pip

WORKDIR /src

RUN pip3 install asyncio nest-asyncio pyserial-asyncio paho-mqtt

WORKDIR /data

# Copy data for add-on
COPY src /

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
