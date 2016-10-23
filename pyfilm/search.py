#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as BS # for parsing html and getting links
from hurry.filesize import size # to display filesize in MB instead of bytes
from pyprind import ProgBar # a progress bar
from google import search_google # import our google search 
from conf import * # our configuration
import requests as r # for getting html files
import pandas as pd # for parsing results.csv
import sys # for any system commands
import re # for regexing

__version__ = '1.1'
__maintainer__ = "jamiejackherer@gmail.com"
__status__ = "In Development"

# Console colors
W = '\033[0m'    # white (normal)
R = '\033[31m'   # red
G = '\033[32m'   # green
O = '\033[33m'   # orange
B = '\033[34m'   # blue
P = '\033[35m'   # purple
C = '\033[36m'   # cyan
GR = '\033[37m'  # gray

# TODO
# -01 truncate link using .format
    
lb = "+--------------------------------------------------------------+" # simple line breaker

def download_film():
    search_google() # search google 
    
    """
    Requests variables.
    """
    s = r.Session() # create an instance of a requests session named 's'
    headers = {"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) Safari/9537.53", 
                "Accept":"text/q=0.9,image/webp,*/*;q=0.8", 
                "Accept-Language":"en-US,en"} # set the user agent and other stuff in the http header 
    
    """
    Variables for get_vodlocker_link function.
    """
    csv_file = "results.csv" # create an instance of the file
    df = pd.read_csv(csv_file) # read said file
    vodlocker_link = df['link'] # get the vodlocker links from the file (note: you can also use df.['column-name']
    link_id = df['title']
    results = df['num_results_for_query']
    results_lower = results[0].lower()
     
    def get_vodlocker_link():               
        print("{0}\n|{1}[+] {2}We have found {3}\n{2}".format(lb, G, W, results_lower)) # print how many links found in how many secs
        print(link_id) # print the title of the pages found as shown in google

    """
    Variables for get_film_link function.
    """
    which_link = input("{0}\n|{1}[?] {3}Which vodlocker link should we use?\n|\n|{2}--> {3}".format(lb, O, B, W))
        
    def get_film_link():        
        while True:
            req = s.get(vodlocker_link[int(which_link)], headers=headers) # get the film link using 'which_link' given by the user and iterate over until we find a valid page with a link in
            bs = BS(req.text, "lxml") # create a soup object
           #file_removed = r"^http?://(*.*.*.*)/([a-zA-Z0-9]\+\)(v.mp4)" 
            # TODO it will be better if we can use a
            # regex search to search for a link 
            # (e.g., http://177.272.45.91/vhxjhvjhv89dyf8w7yrhw9s8eyuf98syfhs89y/v.mp4) 
            # instead of .mp4 
            file_removed = "v.mp4" # if this is not in the page then we dont want this page
            if file_removed not in bs:
                print("{0}\n|{1}[!] {2}We could not find a video file.".format(lb, R, W)) # print no video file
            else:
                break
    
    """
    Variables for find_title function
    """
    film = bs.find(type="video/mp4") # find the film link
    film_link = film["src"] # get the actual film link
    title = bs.find(id="file_title").get_text() # find the title as it is on the vodlocker page
    title_dict() # title_dict from conf file
    regex_title = r"|".join(title_dict) # create a regex 'or' for items in the dict
    fixed_title = re.sub(regex_title, "",title, flags=re.I) # actually remove the items that are in 'title_dict'
    
    def find_title():
        print("{0}\n|{1}[+]{2} The title of the film is:\n|\t{3}".format(lb, G, W, fixed_title)) # print the title with words from 'title_dict' removed
        print("{0}\n|{1}[+]{2} We found a video link on the vodlocker page:\n|\t{3}".format(lb, G, W, film_link)) # 

    """
    Variables for name_film function
    """
    title_lower = fixed_title.lower() # make the title lowercase
    title_strip = title_lower.strip() # strip any white spaces from the lowered title
    title_hyphen = title_strip.replace(" ", "-") # replace any spaces with hyphens
        
    def name_film():     
        ext = film_link[-4:] # use the last 4 chars as the file extension (this should be .mp4 or other video ext.) 
        while True:
            file_name = title_hyphen + ext # name the file by putting 
            file_name_ok = input("{0}\n|{1}[+] {2}We have attempted to name the file from the title; \n|\t\"{3}\"\n|Is our guess O.K? [Yes/no]\n|{4}--> {5}".format(lb, G, W, file_name, B, W)) # ask user if our file_name guess is ok, if no then the user can choose a file_name
            if file_name_ok == 'yes':
                continue
            if file_name_ok != 'yes':
                file_name = input("{0}\n|{1}[+] {2}Please name the file:\n|\n|{3}--> {4}".format(lb, G, W, B, W)) + ext
                continue
            else:
                continue
    
    folder() # we get the folder to save downloads from conf file
    
    def dl_film():    
        u = s.get(film_link, headers=headers, stream=True) # create an instance of the file stream
        file_size = int(u.headers["content-length"]) # get meta info -- file size
        print("{0}\n|{1}[+] {2}File Path and name:\n|\n|\t\"{3}{4}\"".format(lb, G, W, prfx, file_name)) # print the file name and path
        print("{0}\n|{1}[+] {2}File Size: {3}".format(lb, G, W, size(file_size))) # print the file size
        bar = ProgBar(file_size / 1024, title=lb + "\n|" + G + " [+] " + W + "Downloading:\n|\n|" + file_name + "\n" + lb, stream=sys.stdout, bar_char='█', update_interval=1) # Progress bar 
        with open(prfx + file_name, 'wb') as f:
            dl = 0
            if file_size is None: # no content length header
                f.write(r.content)
                print(lb)
                raise Exception("\n|{0}[!] {1}We could not get the total file size (this means there is no data to write to a file).".format(R, W)) # error for no data
            else:
                for chunk in u.iter_content(1024):
                    dl += len(chunk)
                    f.write(chunk)
                    f.flush()
                    bar.update(item_id = file_name)
            print("{0}\n|{1}[+] {2}Finished downloading {3}\n".format(lb, G, W, file_name))
            print(lb)
    
    search_google()
    get_vodlocker_link()
    get_film_link()
    find_title()
    name_film()
    dl_film()
        
download_film()
