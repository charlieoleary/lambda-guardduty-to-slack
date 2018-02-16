FROM python:3.6.4-jessie
MAINTAINER "GlorifiedTypist"

WORKDIR /usr/src

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt &&\
  mkdir ~/.aws &&\
  chmod 700 ~/.aws

COPY ./docker-entrypoint.sh /
COPY troposphere ./troposphere/
COPY src ./src/
COPY tests ./tests/

VOLUME ~/.aws

CMD /bin/bash --login
