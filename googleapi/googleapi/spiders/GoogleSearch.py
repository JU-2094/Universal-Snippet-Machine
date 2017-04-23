#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Spider to extract the urls and data from a request to google
    usage:
        scrapy crawl googlespider -a search='Jose Martínez'
"""
import scrapy
from scrapy.selector import Selector


class GoogleSpider(scrapy.Spider):
    name = "googlespider"
    base_url = "https://www.google.com.mx/"

    def __init__(self,search=None,*args,**kwargs):
        super(GoogleSpider,self).__init__(*args,**kwargs)

        self.log("------------------------")
        self.log(args.__len__())
        if search is not None:
            self.search = search
        else:
            self.search = ""

    def generate_url(self,search):
        pass

    def start_requests(self):
        self.log("----------------------------")
        self.log(self.search)

        yield scrapy.Request(self.base_url,self.parse,cookies={"name":"q","value":self.search})
        # yield scrapy.Request(self.generate_url(self.search),self.parse)

    def parse(self, response):
        self.log("--------------------------------")
        body = response.xpath("//body").extract()
        #self.log(body)
        pass
        #self.log(response.extract())





