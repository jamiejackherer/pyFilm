#!/usr/bin/python3
# We need to rate limit to one request per 3 seconds as gimmeproxy.com
# limits to 20 reqs per second
import requests as req
import time
import json
import csv
    
url = "http://gimmeproxy.com/api/getProxy"
r = req.get(url)
js = r.json()
        
def mk_proxy_list():
    """
    Make a list of proxies, in text format, for google scraper to use.
    
    We do this 30 times to create a longer list.
    """
    def proxy():
        """
        Get the proxy.
        """
        while True:
            with open(r"proxy.json", 'w') as fjson:
                fjson.write(str(js))
    
        """
        Write the proxies to a txt file.
        """     
        while True:
            with open(r"proxies.txt", 'w') as flist:
                flist.write(str(js["curl"] + "\n"))
        
        time.sleep(3)
        proxy() * 30
        
mk_proxy_list()          
