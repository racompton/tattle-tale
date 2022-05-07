# Use an official Python runtime as a parent image
FROM python:3.6-slim

WORKDIR /opt/tattle-tale

RUN mkdir -pv bin etc lib/logstash var/downloads var/tmp

# Install/update system packages
RUN apt-get update ; apt-get -y install libsmi-dev gcc curl cron
RUN pip install elasticsearch-curator
COPY curator/curator.yml curator/delete_old_indices.yml etc/

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# Install our bits & pieces
COPY *.py *.sh bin/
RUN chmod +x bin/*

# RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.13.4-amd64.deb
# RUN dpkg -i filebeat-7.13.4-amd64.deb ; rm filebeat-7.13.4-amd64.deb

# Setup cron to run the update scripts
COPY cron.daily/* /etc/cron.daily/
RUN chmod +x /etc/cron.daily/*
COPY cron.hourly/* /etc/cron.hourly/
RUN chmod +x /etc/cron.hourly/*
RUN touch /var/log/cron.log

CMD /opt/tattle-tale/bin/entrypoint.sh