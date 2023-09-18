import json
import socket


# Function to check if a hostname is an AWS S3 hostname
def contains_s3(hostname):
    return 's3' in hostname


# Load the AWS IP ranges data from the JSON file
with open('ip-ranges.json', 'r') as file:
    aws_ip_ranges = json.load(file)

# Extract all unique regions from the JSON data
unique_regions = set()
for prefix in aws_ip_ranges['prefixes']:
    region = prefix.get('region')
    if region:
        unique_regions.add(region)


# Function to check if a hostname contains any of the unique regions
def contains_region(hostname, regions):
    # Split the hostname by dots to get its parts
    parts = hostname.split('.')

    # Check if any region value appears in the hostname parts
    return any(region in parts for region in regions)


# Read IP addresses from ipaddress.txt and perform DNS lookups
with open('ipaddress.txt', 'r') as ip_file:
    for line in ip_file:
        line = line.strip()  # Remove leading/trailing whitespace
        if not line:
            continue  # Skip empty lines
        ip_to_check = line

        try:
            hostname, _, _ = socket.gethostbyaddr(ip_to_check)
            is_s3 = contains_s3(hostname) or contains_region(hostname, unique_regions)
        except (socket.herror, socket.gaierror):
            is_s3 = False

        if is_s3:
            print(f'{ip_to_check} resolves to an AWS S3 hostname: {hostname}')
        else:
            print('')
