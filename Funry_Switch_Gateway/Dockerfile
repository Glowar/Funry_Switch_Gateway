ARG BUILD_FROM
FROM $BUILD_FROM

# Copy data for add-on
COPY src /

# Install requirements for add-on
RUN \
  apk add --no-cache \
    python3 \
    bash \
    py3-pip

RUN pip3 install -r requirements.txt

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
