FROM docker.elastic.co/beats/filebeat:8.0.0

RUN mv modules.d/netflow.yml.disabled modules.d/netflow.yml
RUN filebeat modules enable netflow
