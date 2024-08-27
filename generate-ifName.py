#!/usr/bin/python3
import csv
import argparse
import socket  # Importing the socket module
import re

# Define a mapping for rpeer name replacements
rpeer_replacements = {
    "LEVEL3": "LUMEN",
    "TELIA": "ARELION",
    "TELECOM_ITALIA": "TELECOM ITALIA",
    "HURRICANE_ELECTRIC": "HURRICANE ELECTRIC",
    # Add more replacements here if needed
}

def resolve_to_ip(router_name):
    """
    Resolves router_name to an IP address using DNS, appending '.comcast.net' if necessary.
    """
    router_name = router_name.strip()
    if not router_name or len(router_name) > 253:
        return None
    if not re.match(r'^[a-zA-Z0-9.-]+$', router_name):
        return None
    if router_name.startswith('-') or router_name.endswith('-'):
        return None
    if not router_name.endswith(".comcast.net"):
        router_name += ".comcast.net"
    
    try:
        return socket.gethostbyname(router_name)
    except (socket.gaierror, UnicodeError):
        return None

def read_asns(asn_file):
    """
    Reads ASNs from a file and returns them as a set for quick lookup.
    """
    with open(asn_file, 'r') as file:
        return {line.strip() for line in file if line.strip()}

def extract_info(input_file, output_file, asn_file):
    """
    Extracts and formats interface information from the input CSV file and writes it to the output file.
    """
    asns = read_asns(asn_file)
    with open(input_file, mode='r', encoding='utf-8') as infile, \
         open(output_file, mode='w', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        for row in reader:
            description = row.get('description', '').strip()
            snmp_index = row.get('snmp_index', '').strip()
            
            if not description or not snmp_index:
                continue  # Skip rows with missing essential information
            
            rpeer = ''
            rasn = ''
            comment = ''
            rhost = ''
            
            # Extract key-value pairs from the description
            for part in description.split('-'):
                if ':' in part:
                    key, value = map(str.strip, part.split(':', 1))
                    key_lower = key.lower()
                    value_stripped = value.strip()
                    
                    if key_lower == 'rpeer':
                        rpeer = value_stripped.upper()
                    elif key_lower == 'rasn':
                        rasn = value_stripped
                    elif key_lower == 'comments':
                        comment = value_stripped
                    elif key_lower == 'rhost':
                        rhost = value_stripped.lower()
            
            # Determine rpeer based on rhost prefixes
            if rhost.startswith(("ceg", "rur", "rar", "sur", "xar")):
                rpeer = "CRAN CUSTOMER"
            elif rasn and rasn in asns:
                rpeer = "COMCAST"
            elif not rpeer and comment:
                rpeer = comment.upper()
            
            # Apply rpeer name replacements
            rpeer = rpeer_replacements.get(rpeer, rpeer)
            
            # Skip processing if rpeer is not defined
            if not rpeer:
                continue  # Skip this entry
            
            # If rpeer is defined, proceed to DNS resolution
            router_name = row.get('router_name', '').strip()
            if not router_name:
                continue  # Skip if router_name is missing

            router_name_ip = resolve_to_ip(router_name)
            if not router_name_ip:
                continue  # Skip if DNS resolution fails
            
            # Construct the output line
            if rasn:
                output_line = f'"{router_name_ip}::ifName.{snmp_index}": "{rpeer} ASN{rasn}"\n'
            else:
                output_line = f'"{router_name_ip}::ifName.{snmp_index}": "{rpeer}"\n'
            
            outfile.write(output_line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract and format interface information from a CSV file.')
    parser.add_argument('--input_file', type=str, required=True, help='Path to the input CSV file')
    parser.add_argument('--output_file', type=str, required=True, help='Path to the output file')
    parser.add_argument('--asn_file', type=str, required=True, help='Path to the ASN list file')
    
    args = parser.parse_args()
    extract_info(args.input_file, args.output_file, args.asn_file)
