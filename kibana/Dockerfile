ARG ELASTIC_VERSION

# https://www.docker.elastic.co/
FROM docker.elastic.co/kibana/kibana:${ELASTIC_VERSION}

COPY kibana.yml /usr/share/kibana/config/

# Add your kibana plugins setup here
# Example: RUN kibana-plugin install <name|url>
