#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Requirements:
        pip install --upgrade google-api-python-client
        
        Google API key.  AIzaSyD5BYgxBrUFtDAlnAYvhpNhEFxrtdF2LHc 
    Spider to extract the urls and data from a request to google
    usage:
        scrapy crawl googlespider -a search='Jose Martínez'     
        
"""
#Todo: RUTA DE ARCHIVO con querys

import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from googleapiclient.discovery import build
from googleapi.googleapi.GoogleClient import GoogleClient

class GoogleSpider(scrapy.Spider):
    name = "googlespider"
    start_urls = ["https://www.google.com/"]

    def __init__(self,search=None,*args,**kwargs):
        super(GoogleSpider,self).__init__(*args,**kwargs)
        if search is not None:
            self.search = search.replace(" ","+")
        else:
            self.search = ""

    def generate_url(self):
        # url_search = self.base_url + "#q="+self.search

        pass

    #def start_requests(self):
        #yield scrapy.Request(self.base_url,method='POST',self.parse,cookies={"name":"q","value":self.search})
        #yield scrapy.Request(self.generate_url(), self.parse)
        #pass



    def parse(self, response):
        #self.log("--------------------------------")
        #urls = response.xpath("//div[@class='rc']").extract()
        #self.log(urls)

        return scrapy.FormRequest.from_response(response,formdata={'q':'Jorge+Flores'},callback=self.method)

        #self.log(response.xpath("//body").extract())

    def method(self,response):
        self.log("-----------Mirame!!!!!----------")
        #self.log(response.xpath("//body").extract())

        urls = response.xpath("//body").extract()
        self.log(urls)

        for info in urls:
            yield {"data":info}





