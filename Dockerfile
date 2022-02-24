# Use an official Python runtime as a parent image
FROM python:3.6-slim

WORKDIR /opt/tattle-tale

COPY requirements.txt ./
COPY *.py bin/

RUN chmod +x bin/*

RUN mkdir -pv etc lib/logstash var/downloads var/tmp

COPY cron.daily/delete_old_indices.sh cron.daily/tattle_tale_shadow.sh /etc/cron.daily/
RUN chmod +x /etc/cron.daily/delete_old_indices.sh /etc/cron.daily/tattle_tale_shadow.sh

# RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.13.4-amd64.deb
# RUN dpkg -i filebeat-7.13.4-amd64.deb ; rm filebeat-7.13.4-amd64.deb

RUN apt-get update ; apt-get -y install libsmi-dev gcc curl
RUN pip install elasticsearch-curator
COPY curator/curator.yml curator/delete_old_indices.yml etc/

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

