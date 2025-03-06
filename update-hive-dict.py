#!/usr/bin/env python3
import os
import argparse
import asyncio
import websockets
import ssl
import json
import yaml
import logging
from websockets_proxy import Proxy, proxy_connect
from websockets import ConnectionClosed

# Setup command line arguments
arg_parser = argparse.ArgumentParser(description='Script to take hive messages via the websocket and output to a YAML file.')

arg_parser.add_argument('--client-cert', "-cc", required=False, action='store', type=open,
                        help="the client cert file")
arg_parser.add_argument('--ca-cert', "-ca", required=False, action='store', type=open,
                        help="the CA file for validating the server")
arg_parser.add_argument("connect_uri", action='store', help="the uri for the server websocket")
arg_parser.add_argument('--websocket-retry-interval', "-ri", required=False, action='store', type=int, default=30,
                        help="the retry interval for reopening a websocket after close/timeout (in seconds)")
arg_parser.add_argument('--proxy-url', "-pu", required=False, action='store', type=str,
                        help="Specify a proxy server to use to make the websocket connection to the HIVE server")
arg_parser.add_argument('--output-dir', "-o", required=False, action='store', type=str, default='.',
                        help="Specify the output directory for the YAML file")
arg_parser.add_argument('--debug', "-d", action='store_true', help="Enable debug logging")

args = arg_parser.parse_args()

# Setup logging
log_level = logging.DEBUG if args.debug else logging.INFO
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure the output directory exists
if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

# Define the output file path
output_file_path = os.path.join(args.output_dir, "hive.yml")

websocket = None
event_loop = None

async def connect_client():
    global event_loop
    global websocket
    # SSL context setup if client and CA certs are provided
    if args.client_cert:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.load_cert_chain(args.client_cert.name)
        ssl_context.load_verify_locations(cafile=args.ca_cert.name)
        ssl_context.verify_mode = ssl.VerifyMode.CERT_REQUIRED
        ssl_context.check_hostname = False
    else:
        ssl_context = None

    try:
        # Proxy setup if specified
        if args.proxy_url:
            proxy = Proxy.from_url(args.proxy_url)
            ws_context = proxy_connect(args.connect_uri, ssl=ssl_context, proxy=proxy)
        else:
            ws_context = websockets.connect(args.connect_uri, ssl=ssl_context, timeout=10)
    except Exception as Ex:
        logging.error(f"Error during connection setup: {Ex}")
        exit(-1)

    event_loop = asyncio.get_event_loop()

    while True:
        try:
            async with ws_context as ws:
                websocket = ws
                logging.info("Connected to the websocket")
                while True:
                    message = await ws.recv()
                    logging.debug(f"Received message: {message}")
                    process_hive_message(message)
        except ConnectionClosed:
            logging.warning("WebSocket connection closed, retrying...")
        except Exception as Ex:
            logging.error(f"Error during message handling: {Ex}")
        finally:
            await asyncio.sleep(args.websocket_retry_interval)

def process_hive_message(message):
    try:
        message_json = json.loads(message)
        message_type = message_json['message']['messageType']
        logging.debug(f"Processing message type: {message_type}")
        if message_type in ['HIVE:ATTACK_START', 'HIVE:ATTACK_END']:
            process_hive_attack_message(message_json['message'])
    except Exception as Ex:
        logging.error(f"Error processing message: {Ex}")

def process_hive_attack_message(hive_message):
    try:
        message_type = hive_message['messageType']
        ip_address = hive_message.get('srcNetwork')
        logging.debug(f"Processing attack message: {message_type}, IP: {ip_address}")
        # Extract the first three octets
        first_three_octets = '.'.join(ip_address.split('.')[:3])

        # Read the existing data or initialize a new dictionary
        if os.path.exists(output_file_path):
            with open(output_file_path, 'r') as file:
                try:
                    data = yaml.safe_load(file) or {}
                except yaml.YAMLError:
                    data = {}
        else:
            data = {}

        # Update the dictionary based on the message type
        if message_type == 'HIVE:ATTACK_START':
            data[first_three_octets] = "hive"
        elif message_type == 'HIVE:ATTACK_END' and first_three_octets in data:
            del data[first_three_octets]

        # Manually construct YAML content with double quotes
        yaml_content = "\n".join(f'"{key}": "{value}"' for key, value in data.items())

        # Write the manually constructed YAML content to the file
        with open(output_file_path, 'w') as file:
            file.write(yaml_content)
    except Exception as Ex:
        logging.error(f"Error processing attack message: {Ex}")

# Clear out the file of old entries when starting up
def clear_output_file():
    """Clears the contents of the output file."""
    logging.info("Clearing the output file.")
    open(output_file_path, 'w').close()

async def main():
    # Call the function to clear the file at the start of the script
    clear_output_file()
    await connect_client()

if __name__ == "__main__":
    asyncio.run(main())
