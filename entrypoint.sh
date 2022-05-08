#!/usr/bin/env bash

set -eu

echo "Fetching current ShadowServer report..."
/opt/tattle-tale/bin/tattle_shadow.py
echo "Completed processing ShadowServer report (return code $?)."

# TODO: Fetch IP report from DIS

echo "TattleTale status at $(date): STARTED"
cron -f

echo "exited $0"