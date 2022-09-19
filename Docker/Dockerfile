# FROM ubuntu:20.04
FROM python:3.10.7-bullseye

RUN apt-get update

# Docker image 빌드 시 Timezone 설정(UTC -> KST)
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
RUN apt-get install -y tzdata

RUN apt-get install -y vim

RUN mkdir ~/jiyeon # 작업 디렉터리 생성

WORKDIR /jiyeon

# WORKDIR /tmp # 작업 경로 설정

RUN pip install --upgrade pip

RUN pip install -U requests datetime beautifulsoup4 pyyaml

COPY KoreaStockAutoTrade.py ./KoreaStockAutoTrade.py

COPY config.yaml ./config.yaml

ENTRYPOINT [ "python", "KoreaStockAutoTrade.py"]

# keeping a Docker container alive
# ENTRYPOINT ["tail", "-f", "/dev/null"]