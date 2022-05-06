ARG ELASTIC_VERSION

# https://www.docker.elastic.co/
FROM docker.elastic.co/logstash/logstash:${ELASTIC_VERSION}

COPY logstash.yml /usr/share/logstash/config/
COPY pipelines.yml /usr/share/logstash/config/
RUN mkdir -p /usr/share/logstash/tattle-tale/

# Add your logstash plugins setup here
# Example: RUN logstash-plugin install logstash-filter-json
