FROM alpine:edge

ARG packages=
ARG entrypoint=/usr/bin/bash

ENV entrypoint=$entrypoint

RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && \
  apk add --no-cache $packages

RUN addgroup --gid 1000 appgroup \
  && adduser appuser \
    --disabled-password \
    --uid 1000 \
    --ingroup appgroup

USER appuser
WORKDIR /home/appuser

ENTRYPOINT "${entrypoint}"
