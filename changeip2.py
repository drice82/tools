#!/usr/bin/env python

import socket
import time
import boto3

ipaddr = 'gp1.ip.com'
ipport = 443
instance_name = 'Ubuntu-1GB-Singapore-1'

def main():
    print("Checking if your IP has been blocked by GFW")
    if ip_status(ipaddr, ipport):
        print("IP is OK")
        exit(0)
    else:
        time.sleep(3)
        if ip_status(ipaddr, ipport):
            print("IP is OK")
            exit(0)
        else:
#            changeip(instance_name)
            print("IP has been blocked, Changing your IP")
            ipv4 = changeip(instance_name)

    exit()
	
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

def changeip(instance_name):
    client = boto3.client('lightsail')
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
    public_ip = response["instance"]["publicIpAddress"]
    print ("Your new public ip is " public_ip)
    return public_ip


if __name__ == '__main__':
    main()
