#!/usr/bin/env bash

set -eu

echo "Fetching current ShadowServer report..."
/opt/tattle-tale/bin/tattle_shadow.py
echo "Completed processing ShadowServer report (return code $?)."

# TODO: Fetch IP report from DIS

cron
echo "TattleTale status at $(date): STARTED"
tail -f /var/log/cron.log
# Perform any cleanup here

echo "exited $0"