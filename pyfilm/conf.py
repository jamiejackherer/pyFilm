#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This is the basic film-search configuration file.
"""

def folder():
    # Change this to choose download folder
    prfx = "downloaded_files" # prefix for file_name location
    
def title_dict():
    # Change this to choose dict file
    title_dict = set(open('title_dict.txt').read().split()) # a dict for common words to remove from the title
