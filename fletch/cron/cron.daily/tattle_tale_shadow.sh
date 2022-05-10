#!/bin/sh

# Run the script to pull down the shadowserver files and then create dictionary files for each
# The logstash filters then use this to filter out events

/opt/tattle-tale/bin/tattle_shadow.py
