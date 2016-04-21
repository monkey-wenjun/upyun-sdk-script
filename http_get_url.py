#!/usr/bin/env python
import requests
import time

def http_get_url():
    srcpath = "D:\suntimereport_file.txt" 
    dstpath = "D:\save.txt"
    serverName = "suntimereport"
    file_str = open(dstpath, 'wb')
    count = 0
    with open(srcpath,'r') as f:
	    for url_path in f:
	        starttime =  time.time()
	        try:
	        	url = "http://"+serverName+".b0.upaiyun.com"+url_path.strip('\n')
	        	req_url = requests.head(url,timeout=5)
	        except Exception,e:
	        	print e
	        endtime =  time.time()
	        count +=1
	        times = round(endtime-starttime,2)
		restatus = req_url.status_code
	        print count,url,times		
		print restatus
	    		if restatus == 404:
				 file_str.write(url)

    file.close()
    file_str.close()


http_get_url()
