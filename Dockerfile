FROM --platform=linux/amd64 golang:1.23-alpine3.20 as builder
RUN apk add --no-cache nodejs npm

ENV GOPATH /gopath/
ENV PATH $GOPATH/bin:$PATH

ARG TAG=v3.1.0
RUN apk add --no-cache curl bash git make

WORKDIR /gopath/src/k8s.io
RUN git clone https://github.com/prometheus/prometheus.git && cd prometheus && git fetch origin tag $TAG && git checkout $TAG # legit:ignore-pipeline
WORKDIR /gopath/src/k8s.io/prometheus

RUN go get github.com/golang-jwt/jwt/v5@v5.2.2 && go get golang.org/x/crypto@v0.35.0 && go mod tidy

RUN make build

FROM quay.io/prometheus/busybox-linux-amd64@sha256:f173c44fab35484fa0e940e42929efe2a2f506feda431ba72c5f0d79639d7f55
LABEL maintainer="The Prometheus Authors <prometheus-developers@googlegroups.com>"

COPY --from=builder /gopath/src/k8s.io/prometheus/promtool /bin/promtool
COPY --from=builder /gopath/src/k8s.io/prometheus/prometheus /bin/prometheus
COPY --from=builder /gopath/src/k8s.io/prometheus/documentation/examples/prometheus.yml /etc/prometheus/prometheus.yml

RUN mkdir -p /prometheus && \
    chown -R nobody:nobody etc/prometheus /prometheus

USER       nobody
EXPOSE     9090
VOLUME     [ "/prometheus" ]
ENTRYPOINT [ "/bin/prometheus" ]
CMD        [ "--config.file=/etc/prometheus/prometheus.yml", \
             "--storage.tsdb.path=/prometheus" ]
