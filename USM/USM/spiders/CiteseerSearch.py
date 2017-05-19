#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    USM -> Universal Snippet Machine

    Spider to extract data from google
    usage:
        scrapy crawl bingspider -a file='path_to_queries_file' 
"""
import scrapy
from scrapy.http import FormRequest,Request
from scrapy import Selector
from USM.items import UsmItem

__author__ = "Josué Fabricio Urbina González"

class CiteSearch(scrapy.Spider):
    name = "citespider"
    start_urls = ["http://citeseerx.ist.psu.edu/"]

    def __init__(self, file=None, *args, **kwargs):
        super(CiteSearch, self).__init__(*args, **kwargs)
        if file is not None:
            self.file = file
        else:
            self.file = ""

    def parse(self, response):
        search = "Jorge Flores"
        yield FormRequest.from_response(response,
                                        formdata={'q': search},
                                        callback=self.cite_selector)

    def cite_selector(self, response):

        base_url = "http://citeseerx.ist.psu.edu/"
        snippets = response.xpath("//div[@class='result']").extract()
        itemproc = self.crawler.engine.scraper.itemproc

        for snippet in snippets:
            storage_item = UsmItem()

            title = Selector(text=snippet).xpath("//h3/a/text()").extract()
            tmpTitle = Selector(text=snippet).xpath("//div[@class='pubinfo']")
            cite = Selector(text=snippet).xpath("//h3/a/@href").extract()
            text = Selector(text=snippet).xpath("//div[@class='snippet']/text()").extract()

            if title.__len__() > 0:
                title = title[0]
                for s in ["authors","pubvenue","pubyear"]:
                    tmp = Selector(text=snippet)\
                        .xpath("//div[@class='pubinfo']/span[@class='"+s+"']/text()")\
                        .extract()

                    if tmp.__len__()>0:
                        title = title + tmp
            else:
                title = ""

            if cite.__len__() > 0:
                #Todo check the url
                cite = self.base_url + cite[0]
            else:
                cite=""

            if text.__len__() > 0:
                text = text[0]
            else:
                text=""

            if cite != "":
                self.log("------------TITLE----------------")
                self.log(title)
                self.log("------------CITE------------------")
                self.log(cite)
                self.log("------------TEXT------------------")
                self.log(text)

                storage_item['title'] = title
                storage_item['cite'] = cite
                storage_item['text'] = text

                itemproc.process_item(storage_item, self)
