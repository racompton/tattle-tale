#!/usr/bin/env python3

import os
import re
import json
import importlib
from datetime import datetime,timezone,timedelta
from urllib.request import urlretrieve
api = importlib.import_module('call-api')
import pandas as pd

# Diretory to temporarily store the downloaded files
dir = '/tmp/shadowserver/'

# Directory where the logstash dictionaries should go

logstash_dir = '/etc/logstash/dictionaries/'
#logstash_dir = '/tmp/shadowserver/dictionaries/'

# Make sure these directories exist and if not, make them:
if not os.path.exists(dir):
    os.makedirs(dir)
if not os.path.exists(logstash_dir):
    os.makedirs(logstash_dir)


# This function downloads all the reports for yesterday using Shadowserver's API
def download_reports(dir):

    # Get the datetime of yesterday
    dt = datetime.now(timezone.utc) - timedelta(days=1)

    # Make the API call to get a list of all the reports
    result = api.api_call('reports/list', { 'date':dt.strftime("%Y-%m-%d") })

    # Put the list of reports into a dictionary
    reports = json.loads(result)

    # For each report in the list of reports, download it to the specified directory
    for report in reports:
        file = os.path.join(dir, report['file'])
        #print('Downloading'+report['file']+' to'+file)
        urlretrieve('https://dl.shadowserver.org/' + report['id'], file)
 

# Fuction to exctract the second column from each report (the IP addresses) and then save the list of IPs to a yaml file to be used by logstash
def make_dicts(dir,logstash_dir):
    for filename in os.listdir(dir):
       if filename.endswith('.csv'):
           # Do regex on filename
           service_name = re.search("\d+-\d+-\d+[_-](.+?)-", filename)
           # open the CSV file
           # print('Opening '+dir+filename)
           # read the CSV file using Pandas
           df = pd.read_csv(dir+filename, low_memory=False)
           
           # Look to see if there is a column called src_ip or ip 
           if "ip" in df.columns:
               # Extract the "ip" column from the dataframe and write to a separate file
               ip_values = df["ip"]
           elif "src_ip" in df.columns:
               ip_values = df["src_ip"]

           # If the service_name starts with "scan_" then remove it!
           service = remove_scan(service_name.group(1))
           # Generate the output filename
           # print('Regex match of '+service_name.group(1))
           output_filename = logstash_dir+service+".yml"
           #print('Generated output filename '+output_filename)

           # Open the output file for writing
           with open(output_filename, 'w') as output_file:
           # iterate over each row and write each line to a file
               #print('Writing to '+output_filename)
               for ip in ip_values:
                       #print('IP is '+ip)
                       #print('Regex match is '+str(service_name.group(1)))
                       line = '"'+str(ip)+'": "'+service+'"'
                       #print('Writing line: '+line)
                       output_file.write(line+'\n')


# Function that deletes all files in the directory
def del_files_in_dir(dir):
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path} with error: {e}")

def remove_scan(string):
    if string.startswith("scan_"):
        return string[5:]
    return string


if __name__ == '__main__':

    # Delete all files in the temp directory
    del_files_in_dir(dir)

    # Download the reports to the directory
    download_reports(dir)

    # Generate the Logstash Dictionary YML files
    make_dicts(dir,logstash_dir)
