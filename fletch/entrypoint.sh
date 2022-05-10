#!/usr/bin/env bash

set -eu

echo "Fetching current ShadowServer report..."
/opt/tattle-tale/bin/tattle_shadow.py
echo "Completed processing ShadowServer report (return code $?)."

# TODO: Fetch IP report from DIS
echo "Cron schedule:"
crontab -l

echo "TattleTale status at $(date): STARTED"
echo "Starting cron..."
cron -f -L 8

echo "exited $0"