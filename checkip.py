#!/usr/bin/env python

import socket
import time

def main():
    print(ip_status('www.baidu.com',8080))
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

if __name__ == '__main__':
    main()
