# /usr/bin/env python
# -*- coding: utf8 -*-
"""
    Requirements:
        pip install --upgrade google-api-python-client
    
"""

__author__ = "Josué Fabricio Urbina González"

import pprint
import logging as log
import threading
from googleapiclient.discovery import build
#ToDo storage the json recovered

class GoogleClient(threading.Thread):
    key = "AIzaSyD5BYgxBrUFtDAlnAYvhpNhEFxrtdF2LHc"
    customEngine = '017834202398449870076:eeqbhmbsv90'
    max_queries = 100   #The API allows 100 per day

    def __init__(self,search):
        threading.Thread.__init__(self)
        self.search = search
        self.service = build("customsearch", "v1",
                             developerKey=self.key)

    def run(self):
        log.INFO("Getting json from customsearch api")
        self._getjson()
        log.INFO("End of THREAD")

    def _getjson(self):
        start = 1
        try:
            while True:
                res = self.service.cse().list(
                    q=self.search,
                    cx=self.customEngine,
                    start=str(start)
                ).execute()

                yield res

                start = start + 10
                if start > self.max_queries:
                    break
        except:
            log.error(" API_GOOGLE CUSTOM_SEARCH: %s", "Cuote of 100 queries per day surpased")
            return None