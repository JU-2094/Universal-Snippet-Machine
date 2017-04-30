#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Requirements:
        pip install --upgrade google-api-python-client
    Spider to extract the urls and data from a request to google
    usage:
        scrapy crawl googlespider -a search='path_to_queries_file' 
    
    Notes. In PyCharm, the directories must be marked as sources root
"""
#Todo: RUTA DE ARCHIVO con querys

import scrapy
from scrapy.selector import Selector
from scrapy.http import Request,FormRequest
from googleapi.GoogleClient import GoogleClient

class GoogleSpider(scrapy.Spider):
    name = "googlespider"
    base_url = "https://www.google.com/"
    start_urls = ["https://www.google.com/"]

    def __init__(self,search=None,*args,**kwargs):
        super(GoogleSpider,self).__init__(*args,**kwargs)

        ##Todo Adapt this to the path
        if search is not None:
            self.search = search.replace(" ","+")
        else:
            self.search = ""

    def get_query(self):
        # Todo from file get the search queries
        yield 'Jorge+Flores'

    def parse(self, response):
        for query in self.get_query():
            yield FormRequest.from_response(response,formdata={'q':query},callback=self.collect_snippet)

    def collect_snippet(self,response):
        snippets = response.xpath("//div[@class='g']").extract()

        for snippet in snippets:
           #Todo Create json or fill DB
           pass

        for url in response.xpath("//td[@class='b']/a/@href").extract():
            yield Request(self.base_url+url, callback=self.collect_snippet)
