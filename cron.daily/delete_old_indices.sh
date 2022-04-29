#!/bin/sh

# Script to delete elasticsearch netflow-* indicies older than 45 days
# Put this file in /etc/cron.daily/ and make sure it's executable (chmod 755 delete_old_indicies.sh)

/usr/local/bin/curator /opt/tattle-tale/etc/delete_old_indices.yml --config /opt/tattle-tale/etc/curator.yml
