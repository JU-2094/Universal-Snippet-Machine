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


class DuckSearch(scrapy.Spider):
    name = "duckspider"
    start_urls = ["https://duckduckgo.com/"]

    def __init__(self, file=None, *args, **kwargs):
        super(DuckSearch, self).__init__(*args, **kwargs)
        if file is not None:
            self.file = file
        else:
            self.file = ""

    def parse(self, response):
        search = "Jorge Flores"
        yield FormRequest.from_response(response,
                                        formdata={'q': search},
                                        callback=self.duck_selector)

    def duck_selector(self, response):

        base_url = "https://duckduckgo.com/"
        snippets = response\
            .xpath("//div[@class='result results_links results_links_deep web-result ']")\
            .extract()
        itemproc = self.crawler.engine.scraper.itemproc

        for snippet in snippets:
            storage_item = UsmItem()

            title = Selector(text=snippet).xpath("//h2[@class='result_title']/a/text()").extract()
            cite = Selector(text=snippet).xpath("//a[@class='result_snippet']/@href").extract()
            text = Selector(text=snippet).xpath("//a[@class='result_snippet']/text()").extract()

            if title.__len__()>0:
                title = title[0]
            else:
                title = ""

            if cite.__len__()>0:
                cite = cite[0]
            else:
                cite=""

            if text.__len__()>0:
                text = text[0]
            else:
                text = ""

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

