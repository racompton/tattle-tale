#!/usr/bin/python3

# This is a script to take the csv output of interface data from Arbor's Sightline database
# and then it generates a dictionary file for Logstash to use.

import csv
import argparse
import socket

# Function for resolving router_name to an IP address using DNS, with conditional domain appending
def resolve_to_ip(router_name):
    if not router_name.endswith(".comcast.net"):
        router_name += ".comcast.net"
    try:
        return socket.gethostbyname(router_name)
    except socket.gaierror:
        return None

# Function to read ASNs from a file and return them as a set
def read_asns(asn_file):
    with open(asn_file, 'r') as file:
        return {line.strip() for line in file}

# Function to extract and format the required information with command-line arguments
def extract_info(input_file, output_file, asn_file):
    asns = read_asns(asn_file)
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        for row in reader:
            if 'rasn' in row['description']:
                router_name_ip = resolve_to_ip(row['router_name'])
                if router_name_ip:
                    snmp_index = row['snmp_index']
                    rpeer = rasn = comment = ""
                    for part in row['description'].split('-'):
                        if ':' in part:
                            key, value = part.split(':', 1)
                            key, value = key.strip(), value.strip()
                            if 'rpeer' == key:
                                rpeer = value.upper()
                            elif 'rasn' == key:
                                rasn = value
                            elif 'comments' == key:
                                comment = value
                    rpeer = rpeer if rpeer else comment.upper()
                    if rasn in asns:
                        rpeer = "COMCAST"
                    if not rpeer:
                        rpeer = "COMCAST CRAN"
                    outfile.write(f'"{router_name_ip}::ifName.{snmp_index}": "{rpeer} ASN{rasn}"\n')
                else:
                    print(f"DNS resolution failed for {row['router_name']}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract and format interface information from a CSV file.')
    parser.add_argument('--input_file', type=str, required=True, help='Location of the input CSV file')
    parser.add_argument('--output_file', type=str, required=True, help='Location to output the ifName.yml file')
    parser.add_argument('--asn_file', type=str, required=True, help='Location of the ASN list file')

    args = parser.parse_args()

    extract_info(args.input_file, args.output_file, args.asn_file)
