ARG ELASTIC_VERSION

FROM docker.elastic.co/beats/filebeat:${ELASTIC_VERSION}

RUN mv modules.d/netflow.yml.disabled modules.d/netflow.yml
RUN filebeat modules enable netflow
RUN sed -i "s/enabled: false/enabled: true/g" modules.d/netflow.yml
RUN sed -i "s/netflow_host: localhost/netflow_host: 0.0.0.0/g" modules.d/netflow.yml

COPY filebeat.yml ./

CMD filebeat -e -c ./filebeat.yml --path.home /usr/share/filebeat --path.config /usr/share/filebeat