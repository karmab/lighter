FROM alpine:3.10

MAINTAINER Karim Boumedhel <karimboumedhel@gmail.com>

LABEL name="karmab/ligher" \
      maintainer="karimboumedhel@gmail.com" \
      vendor="Karmalabs" \
      version="latest" \
      release="0" \
      summary="Evaluate which ignition a node should use" \
      description="Evaluate which ignition a node should use"

EXPOSE 9000

RUN apk add python3 gcc musl-dev python3-dev
RUN pip3 install flask kubernetes
ADD main.py /

ENTRYPOINT  ["python3", "-u", "/main.py"]
