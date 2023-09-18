import json
import socket

# Load the AWS IP ranges data from the JSON file
with open('ip-ranges.json', 'r') as file:
    aws_ip_ranges = json.load(file)


# Function to check if a hostname is an AWS S3 hostname
def contains_s3(hostname):
    return 's3' in hostname or 'aws' in hostname



# Read IP addresses from ipaddress.txt and perform DNS lookups
with open('ipaddress.txt', 'r') as ip_file:
    for line in ip_file:
        ip_to_check = line.strip()  # Remove leading/trailing whitespace

        try:
            hostname, _, _ = socket.gethostbyaddr(ip_to_check)
            is_s3 = contains_s3(hostname)
        except (socket.herror, socket.gaierror):
            is_s3 = False

        if is_s3:
            print(f'{ip_to_check} resolves to an AWS S3 hostname: {hostname}')
        else:
            print("")
