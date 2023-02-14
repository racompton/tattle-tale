#!/bin/sh

# Run the script to pull down the shadowserver files and then create dictionary files for each
# The logstash filters then use this to filter out events

/opt/tattle_tale/download-shadowserver-reports.py

# Generate a dictionary file for the entries from dissarm.net for the last day
# /opt/tattle_tale/get-dissarm-ips.py -k <API key> -o <Org ID> -d 1 -f /etc/logstash/dictionaries/dis-abusesrs.yml
