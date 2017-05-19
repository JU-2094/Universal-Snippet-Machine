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

class BingSearch(scrapy.Spider):

    name = "bingspider"
    start_urls = ["https://www.bing.com/"]

    def __init__(self, file=None, *args, **kwargs):
        super(BingSearch, self).__init__(*args, **kwargs)
        if file is not None:
            self.file = file
        else:
            self.file = ""

    def parse(self, response):
        search = "Jorge Flores"
        yield FormRequest.from_response(response,
                                        formdata={'q': search},
                                        callback=self.bing_selector)

    def bing_selector(self, response):
        base_url = "https://www.bing.com/"
        snippets = response.xpath("//li[@class='b_algo']").extract()
        itemproc = self.crawler.engine.scraper.itemproc

        for snippet in snippets:
            storage_item = UsmItem()
            title = Selector(text=snippet).xpath("//h2/a/node()").extract()
            cite = Selector(text=snippet).xpath("//h2/a/@href").extract()
            text = Selector(text=snippet).xpath("//p").extract()

            tmp_title = ""
            for cad in title:
                tmp_title = tmp_title+cad
            for r in ["<strong>", "</strong>"]:
                tmp_title = tmp_title.replace(r,'')
            title = tmp_title

            if cite.__len__()>0:
                cite = cite[0]
            else:
                cite = ""

            if text.__len__()>0:
                text = text[0]
                for r in ["<p>", "</p>", "<strong>", "</strong>"]:
                    text = text.replace(r, '')
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

                itemproc.process_item(storage_item,self)
        number = response.xpath("//li[@class='b_pag']/nav[@role='navigation']"
                                "//a[@class='sb_pagS']/text()").extract()
        self.log("-----------NUMBER OF PAGE-----")
        if number.__len__() > 0:
            self.log(number[0]+"")
            if int(number[0]) < 4:
                num = int(number[0])+1
                num = str(num)
                res = response.xpath("//li[@class='b_pag']/nav[@role='navigation']"
                                     "//a[@aria-label='Page "+num+"']/@href").extract()
                for url in res:
                    self.log("--URL TO FOLLOW--")
                    self.log(base_url + url)
                    # return Request(base_url + url, callback=self.collect_snippet)
                    yield Request(base_url + url, callback=self.bing_selector)
