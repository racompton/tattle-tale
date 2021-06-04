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

# Temporary directory to store new dictionaries
# Must include the trailing /
shadow_temp_dir = "/opt/tattle_tale/dicts/"

# Dictionary location for Logstash
# Must include the trailing /
logstash_dict_dir = "/etc/logstash/dictionaries/"
