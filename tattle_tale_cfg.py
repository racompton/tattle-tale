#!/usr/bin/env python3

# Username for Shadowserver authentication
# TODO: Make envvar
shadow_user = "<username>"

# Password for Shadowserver authentication
# TODO: Make envvar
shadow_pass = "<password>"

# URL for Shadowserver download list
shadow_url = "https://dl.shadowserver.org/reports/index.php"

# Directory to store Shadowserver downloads
# Must include the trailing /
shadow_dir = "/opt/tattle-tale/var/downloads/"

# Directory to store new dictionaries
# Must include the trailing /
shadow_temp_dir = "/opt/tattle-tale/var/tmp/"

# Dictionary location for Logstash
# Must include the trailing /
logstash_dict_dir = "/opt/tattle-tale/lib/logstash/"

# File containing list of IP addresses to query via SNMP
# TODO: Make envvar pointing to host file
# Can be config variable?
# Potentially support run-time modification?
device_list = "/opt/tattle-tale/etc/router-list.txt"

# SNMPv2c community string
# TODO: Make envvar
snmp_community = "<community string>"

# Regular Expression to pull Peer name from interface description
# Change to match your naming convention
# BTW, https://regex101.com is really good for testing regex
# TODO: Make envvar
if_regex = "\[NAME=(.+?)\]"

