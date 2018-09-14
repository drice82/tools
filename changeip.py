#!/usr/bin/env python
#
# CloudFlare DDNS script.
#
# usage:
#   cloudflare_ddns.py [config]
#
# See README for details
#
import socket
import string
import math
import requests
import json
import time
import yaml
import os
import sys
import collections
import boto3
from subprocess import Popen, PIPE

# CloudFlare api url.
CLOUDFLARE_URL = 'https://api.cloudflare.com/client/v4'

# Time-to-live for your A record. This should be as small as possible to ensure
# changes aren't cached for too long and are propogated quickly.  CloudFlare's
# api docs set a minimum of 120 seconds.
TTL = '120'

# DNS record type for your DDNS host. Probably an A record.
RECORD_TYPE = 'A'

# Location of this script.
SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))

# If a command-line argument is provided, use that as the config file.
if len(sys.argv) == 1:
    CONFIG_FILE = os.path.join(SCRIPT_ROOT, "config.yaml")
else:
    CONFIG_FILE = os.path.join(SCRIPT_ROOT, sys.argv[1])


def main():
    print(aws())
    return

def aws():
    client = boto3.client('lightsail')
    client.detach_static_ip(
        staticIpName='StaticIp-Singapore-2'
    )

    client.release_static_ip(
        staticIpName='StaticIp-Singapore-2'
    )

    client.allocate_static_ip(
        staticIpName='StaticIp-Singapore-2'
    )

    client.attach_static_ip(
        staticIpName='StaticIp-Singapore-2',
        instanceName='Ubuntu-1GB-Singapore-1'
    )

    response = client.get_static_ip(
        staticIpName='StaticIp-Singapore-2'
    )
    return response

def die(msg):
    log('error', msg)
    raise Exception(msg)


if __name__ == '__main__':
    main()
