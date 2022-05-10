#!/usr/bin/env python3

import os

# Username for Shadowserver authentication
shadow_user = os.getenv("TT_SHADOW_USER")

# Password for Shadowserver authentication
shadow_pass = os.getenv("TT_SHADOW_PASS")

# URL for Shadowserver download list
shadow_url = os.getenv("TT_SHADOW_REPORT_URL", default="https://dl.shadowserver.org/reports/index.php")

# Directory to store Shadowserver downloads
# Must include the trailing /
shadow_dir = os.getenv("TT_SHADOW_REPORT_DOWNLOAD_DIR", default="/opt/tattle-tale/var/downloads/")

# Directory to store new dictionaries
# Must include the trailing /
shadow_temp_dir = os.getenv("TT_SHADOW_REPORT_TEMP_DIR", default="/opt/tattle-tale/var/tmp/")

# Dictionary location for Logstash
# Must include the trailing /
logstash_dict_dir = os.getenv("TT_SHADOW_REPORT_DICT_DIR", default="/opt/tattle-tale/lib/logstash/")

# File containing list of IP addresses to query via SNMP
# TODO: Potentially support run-time modification?
device_list = os.getenv("TT_ROUTER_LIST_FILE", default="/opt/tattle-tale/lib/router-list.txt")

# SNMPv2c community string
snmp_community = os.getenv("TT_SNMP_COMMUNITY_STRING")

# Regular Expression to pull Peer name from interface description
if_regex = os.getenv("TT_INT_DESCRIPTION_PEER_NAME_REGEX")

