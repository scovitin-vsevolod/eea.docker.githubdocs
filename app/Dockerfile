FROM python:2.7-slim
MAINTAINER "EEA: IDM2 A-Team" <eea-edw-a-team-alerts@googlegroups.com>
RUN apt-get update -q &&\
    apt-get install build-essential -y &&\
    apt-get install git -y

COPY src /src

RUN pip install -r /src/requirements.txt

WORKDIR /src
ENTRYPOINT ["python", "update_package.py"]
