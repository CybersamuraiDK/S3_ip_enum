import json
import socket

# Load the AWS IP ranges data from the JSON file
with open('ip-ranges.json', 'r') as file:
    aws_ip_ranges = json.load(file)


# Function to check if a hostname is an AWS S3 hostname
def is_s3_hostname(hostname):
    return hostname.endswith('.s3.amazonaws.com')


# Read IP addresses from ipaddress.txt and perform DNS lookups
with open('ipaddress.txt', 'r') as ip_file:
    for line in ip_file:
        ip_to_check = line.strip()  # Remove leading/trailing whitespace

        try:
            hostname, _, _ = socket.gethostbyaddr(ip_to_check)
            is_s3 = is_s3_hostname(hostname)
        except (socket.herror, socket.gaierror):
            is_s3 = False

        if is_s3:
            print(f'{ip_to_check} resolves to an AWS S3 hostname: {hostname}')
        else:
            print("")
