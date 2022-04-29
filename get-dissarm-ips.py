#!/usr/bin/python3
# This script outputs a list of IP addresses genertating outbound DDoS attacks from the dissarm.net API that occured the last X number of days.

import requests
import json
import argparse
import sys
import os

# Make sure we are running Python 3
if sys.version_info<(3,0,0):
   sys.stderr.write("You need python 3.0+ or later to run this script\n")
   exit(1)

# Parse the command line arguments
parser = argparse.ArgumentParser(description='This script outputs a list of IP addresses genertating outbound DDoS attacks from the dissarm.net API that occured the last X number of days.')
parser.add_argument('-k','--key', help='Specify an API key',required=True)
parser.add_argument('-o','--org',help='Specify an Org ID', required=True)
parser.add_argument('-d','--days',help='Specify the number of days of historical info to retrieve', required=True)
parser.add_argument('-f','--file',help='Specify the path and filename of the log file to write', required=False)
parser.add_argument('--debug', action='store_true', help='Enable debug mode',required=False)
args = parser.parse_args()

# Generate the headers, url, and payload
headers={"X-API-Key" : args.key}
url='https://api.dissarm.net/v1/organizations/'+args.org+'/report'
payload = {'lastReportedDays':args.days, 'limit':10000, 'removeSelfReported':'false', 'order': 'count'}
if args.debug:
    print(headers)
    print(payload)
    print(url)

# Make the call to the API
response = requests.get(url, params=payload, headers=headers)

# Put the response into a dict
data = response.json()

if args.debug:
    print(data)

# If the file was specified then open up a new file
if args.file:
    if (os.path.exists(args.file)):
        os.remove(args.file)
    f = open(args.file, "x")

# Get the number of results and iterate through each one
    for i in range(len(data['results'])):
        f.write("\""+data['results'][i]['ipAddress']+"\": \"dis_abuser\"\n")
    f.close()

else:
# Print out IP address of each result
    print(data['results'][i]['ipAddress'])
