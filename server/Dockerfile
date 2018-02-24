FROM ubuntu:16.04

ENV DEV 1

RUN apt-get update && \
	apt-get install -y \
		mysql-client \
		python-pip \
		libmysqlclient-dev \
		build-essential \
		python-dev 

WORKDIR /server
# COPY easykrishi_server/ /server
