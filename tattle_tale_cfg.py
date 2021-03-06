#!/usr/bin/env python3

# Username for Shadowserver authentication
shadow_user = "<username>"

# Password for Shadowserver authentication
shadow_pass = "<password>"

# URL for Shadowserver download list
shadow_url = "https://dl.shadowserver.org/reports/index.php"

# Directory to store Shadowserver downloads
# Must include the trailing /
shadow_dir = "/opt/tattle_tale/downloads/"

# Directory to store new dictionaries
# Must include the trailing /
shadow_temp_dir = "/opt/tattle_tale/dicts/"

# Dictionary location for Logstash
# Must include the trailing /
logstash_dict_dir = "/etc/logstash/dictionaries/"

# File containing list of IP addresses to query via SNMP
device_list = "/opt/tattle_tale/router_list.txt"

# SNMPv2c community string
snmp_community = "<community string>"

# Regular Expression to pull Peer name from interface description
# Change to match your naming convention
# BTW, https://regex101.com is really good for testing regex
if_regex = "\[NAME=(.+?)\]"

