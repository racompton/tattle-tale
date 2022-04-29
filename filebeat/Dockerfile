FROM docker.elastic.co/beats/filebeat:8.0.0

RUN mv modules.d/netflow.yml.disabled modules.d/netflow.yml
RUN filebeat modules enable netflow
RUN sed -i "s/    enabled: false/    enabled: true/g" modules.d/netflow.yml

COPY filebeat.yml ./

CMD filebeat -e -c ./filebeat.yml --path.home /usr/share/filebeat --path.config /usr/share/filebeat