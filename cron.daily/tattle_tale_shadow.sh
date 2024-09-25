#!/bin/sh

# Run the script to pull down the shadowserver files and then create dictionary files for each
# The logstash filters then use this to filter out events

/opt/tattle-tale/download-shadowserver-reports.py

# Generate a dictionary file (dis.yml) for the entries from dissarm.net for the last day
# /opt/tattle_tale/get-dissarm-ips.py -k <API key> -o <Org ID> -d 1 -f /etc/logstash/dictionaries/dis-abusesrs.yml

# Generate a dictionary file (ifName.yml) for the interface names by SNMP polling the routers
# /opt/tattle_tale/tattle_snmp_poll.py 
