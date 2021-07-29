# Use an official Python runtime as a parent image
FROM python:3.6-slim

WORKDIR /opt/tattle-tail

COPY requirements.txt ./
COPY *.py bin/

RUN chmod +x bin/*

RUN mkdir -pv etc lib/logstash var/downloads var/tmp
VOLUME /opt/tattle-tail/lib

RUN apt-get update ; apt-get -y install libsmi-dev gcc curl

RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.13.4-amd64.deb
RUN dpkg -i filebeat-7.13.4-amd64.deb

COPY filebeat/* /etc/filebeat/

# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

