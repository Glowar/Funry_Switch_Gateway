ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN \
  apk add --no-cache \
    python3 \
    bash \
    py3-pip

RUN \
  pip3 install asyncio && \
  pip3 install nest-asyncio && \
  pip3 install pyserial-asyncio && \
  pip3 install paho-mqtt


# Copy data for add-on
COPY src /

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
