import socket
import time
import string
import math
import os
import json
#import collections
#import psutil
import commands

#========自定义的内容==========
#是否被墙
def main():
	print(ip_status())
	
def ip_status():
	#14.215.177.39是百度的ip
	#123.125.115.110 也是百度的ip
	#117.136.190.162 10086的ip

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
