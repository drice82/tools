#!/usr/bin/env python

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

def main():

    print(ip_status())
    exit()

def die(msg):
    log('error', msg)
    raise Exception(msg)

	
def ip_status():
    object_check = ['123.125.115.110', '14.215.177.39', '117.136.190.162']
    ip_check = 0
    for i in object_check:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(1)
	try:
	    s.connect((i, 80))
	    ip_check=1
	    break
	except:
	    continue
	s.close()
    if ip_check==1:
        return True
    else:
        return False

if __name__ == '__main__':
    main()
