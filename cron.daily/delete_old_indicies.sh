#!/bin/sh

# Script to delete elasticsearch netflow-* indicies older than 45 days
# Put this file in /etc/cron.daily/ and make sure it's executable (chmod 755 delete_old_indicies.sh)

/bin/curator /etc/curator/delete_old_indicies.yml --config /etc/curator/curator.yml 
