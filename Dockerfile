FROM python:3.6-alpine3.6
LABEL maintainer="GlorifiedTypist"

WORKDIR /usr/src

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
  mkdir ~/.aws &&\
  chmod 700 ~/.aws

COPY ./docker-entrypoint.sh /
COPY troposphere ./
COPY src ./

VOLUME ["~/.aws"]

CMD ["/docker-entrypoint.sh"]
