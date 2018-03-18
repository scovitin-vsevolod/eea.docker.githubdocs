FROM python:2.7-slim
MAINTAINER "EEA: IDM2 A-Team" <eea-edw-a-team-alerts@googlegroups.com>

RUN apt-get update \
 && apt-get install -y build-essential git vim \
 && rm -rf /var/lib/apt/lists/*

COPY src/requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt

COPY .gitconfig /root/
COPY src /src

WORKDIR /src
ENTRYPOINT ["/src/docker-entrypoint.sh"]
