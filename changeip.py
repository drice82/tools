#!/usr/bin/env python

import socket
import time
import boto3
import string
import math
import requests
import json
import time
import os
import sys
import collections
from subprocess import Popen, PIPE

# CloudFlare api url.
CLOUDFLARE_URL = 'https://api.cloudflare.com/client/v4'

# Time-to-live for your A record. This should be as small as possible to ensure
# changes aren't cached for too long and are propogated quickly.  CloudFlare's
# api docs set a minimum of 120 seconds.
TTL = '120'

# DNS record type for your DDNS host. Probably an A record.
RECORD_TYPE = 'A'


ipaddr = 'us5.node.com'
ipport = 8080
instance_name = 'agw-us1'

aws_key_id = 'AKxxxxxxx7DA'
aws_secret_key = 'UsxxxxxxxG+TF'
aws_region = 'us-west-2'

cf_key = '84xxxxxxxd'
cf_email = 'name@gmail.com'
cf_domain = 'node.com'
cf_subdomain = 'us5'
cf_service_mode = 0
quiet = 'false'
auth_headers = {
    'X-Auth-Key': cf_key,
    'X-Auth-Email': cf_email,
}

def main():
    if ip_status(ipaddr, ipport):
        exit(0)
    else:
        time.sleep(3)
        if ip_status(ipaddr, ipport):
            exit(0)
        else:
            print("IP has been blocked, Changing your IP")
            public_ip = changeip(instance_name)

    ### Get zone id for the dns record we want to update
    results = get_paginated_results(
        'GET',
        CLOUDFLARE_URL + '/zones',
        auth_headers,
    )
    cf_zone_id = None
    for zone in results:
        zone_name = zone['name']
        zone_id = zone['id']
        if zone_name == cf_domain:
            cf_zone_id = zone_id
            break
    if cf_zone_id is None:
        raise Exception("Snap, can't find zone '{}'".format(cf_domain))

    ### Get record id for the record we want to update
    if cf_subdomain == '':
        target_name = cf_domain
    else:
        target_name = cf_subdomain + '.' + cf_domain
    results = get_paginated_results(
        'GET',
        CLOUDFLARE_URL + '/zones/' + cf_zone_id + '/dns_records',
        auth_headers,
    )
    cf_record_obj = None
    for record in results:
        record_id = record['id']
        record_name = record['name']
        if record_name == target_name:
            cf_record_obj = record
            break
    if cf_record_obj is None:
        raise Exception("Snap, can't find record '{}'".format(target_name))

    if not quiet:
        print(json.dumps(cf_record_obj, indent=4))

    ### Update the record
    current_record_ip = cf_record_obj['content']
    if current_record_ip == public_ip:
        # If this record already has the correct IP, we return early
        # and don't do anything.
        if not quiet:
            log('unchanged', '{}, {}'.format(target_name, public_ip))
        return

    cf_record_obj['content'] = public_ip
    r = requests.put(
        CLOUDFLARE_URL
            + '/zones/'
            + cf_zone_id
            + '/dns_records/'
            + cf_record_obj['id'],
        headers=auth_headers,
        json=cf_record_obj
    )
    status_was_error = False
    if r.status_code < 200 or r.status_code > 299:
        log(
            'error',
            "CloudFlare returned an unexpected status code: {}, for "
            "dns_records update request."
            .format(r.status_code)
        )
        status_was_error = True
    response = r.json()
    if response["errors"] or status_was_error:
        die("Updating record failed with the response: '{}'".format(
            json.dumps(response)
        ))
    else:
        log('updated', "{}, {}".format(target_name, public_ip))

    return

	
def ip_status(addr,port):
    ip_check = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((addr, port))
        ip_check=1
    except:
        ip_check=0
    s.close()
    if ip_check==1:
        return True
    else:
        return False


def get_paginated_results(method, url, auth_headers):
    """
    Executes the cloudflare api call, fetches all pages and returns the
    concatenated result array.
    """

    results = []
    page = 0
    total_pages = None
    while page != total_pages:
        page += 1
        r = requests.request(
            method,
            url,
            params={'page': page},
            headers=auth_headers
        )

        if r.status_code < 200 or r.status_code > 299:
            die(
                "CloudFlare returned an unexpected status code: {}, for "
                "request: {}"
                .format(
                    r.status_code,
                    url
                )
            )

        response = r.json()
        results.extend(response['result'])
        total_pages = response['result_info']['total_pages']
    return results



def log(status, message=''):
    print(
        "{date}, {status:>10}, '{message}'".format(
            date=time.ctime(),
            status=status,
            message=message
        )
    )
    return



def die(msg):
    log('error', msg)
    raise Exception(msg)



def changeip(instance_name):
    client = boto3.client(
        'lightsail',
        aws_access_key_id=aws_key_id,
        aws_secret_access_key = aws_secret_key,
        region_name = aws_region,
    )
    print("Stopping your instance, Please wait...")
    client.stop_instance(
        instanceName=instance_name,
        force=False
    )
    time.sleep(60)
    print("Restarting your instance, Please wait...")
    client.start_instance(
        instanceName=instance_name,
    )
    time.sleep(60)
    response = client.get_instance(
        instanceName = instance_name,
    )
    ipv4_ip = response["instance"]["publicIpAddress"]
    print ("Your new public ip is ", ipv4_ip)
    return ipv4_ip


if __name__ == '__main__':
    main()

