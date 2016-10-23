# -*- coding: utf-8 -*-

"""
A Spliff a day keeps the doctor away!
"""

__author__ = 'JamieJackHerer'
__updated__ = '05.06.2016'  # day.month.year

from GoogleScraper.proxies import Proxy
from GoogleScraper.config import get_config
import logging

"""
All objects imported here are exposed as the public API of GoogleScraper
"""

from GoogleScraper.core import scrape_with_config
from GoogleScraper.scraping import GoogleSearchError, MaliciousRequestDetected

logging.getLogger(__name__)
