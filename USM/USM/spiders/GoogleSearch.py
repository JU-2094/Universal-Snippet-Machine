#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    USM -> Universal Snippet Machine

    Spider to extract data from google
    usage:
        scrapy crawl googlespider -a file='path_to_queries_file' 
"""
# Todo: Check the '...' in the cites and the complete url in google snippets

import scrapy
from scrapy import Selector
from scrapy.http import FormRequest,Request
from USM.items import UsmItem
from USM.learntools.BasicTool import Utils

__author__ = "Josué Fabricio Urbina González"


class GoogleSpider(scrapy.Spider):

    name = "googlespider"
    start_urls = ["https://www.google.com.mx/"]

    def __init__(self, file=None, *args, **kwargs):
        super(GoogleSpider, self).__init__(*args, **kwargs)
        if file is not None:
            self.file = file
        else:
            self.file = ""

    def parse(self, response):
        if self.file != "":
            for search in Utils.get_query(Utils(), file=self.file):
                request = FormRequest.from_response(response,
                                                    formdata={'q': search[1]},
                                                    callback=self.google_selector)
                request.meta['search'] = search[0]
                yield request

    def google_selector(self, response):
        base_url = "https://www.google.com.mx/"
        snippets = response.xpath("//div[@class='g']").extract()
        itemproc = self.crawler.engine.scraper.itemproc

        search = response.meta['search']

        for snippet in snippets:
            storage_item = UsmItem()

            title = Selector(text=snippet).xpath("//a/b/text() | //a/text()").extract()
            cite = Selector(text=snippet).xpath("//cite").extract()
            # cite = Selector(text=snippet).xpath("//h3/a/@href").extract()

            text = Selector(text=snippet).xpath("//span[@class='st']").extract()

            if title.__len__() >= 2:
                title = title[0]+title[1]
            else:
                title=""

            if cite.__len__() > 0:
                # cite = cite[0].split("url?q=")[-1]
                cite = cite[0]
                for r in ['<cite>', '</cite>', '<b>', '</b>']:
                    cite = cite.replace(r, '')
            else:
                cite=""

            if text.__len__() > 0:
                text = text[0]
                for r in ['<span class="st">', '</span>', '<br>', '</br>', '<b>', '</b>']:
                    text = text.replace(r, '')
            else:
                text = ""

            if cite != "":
                self.log("----------------TITLE-----------")
                self.log(title)
                self.log("-------------CITE--------------")
                self.log(cite)
                self.log("-------------TEXT--------------")
                self.log(text)
                self.log("----------QUERY----------------")
                self.log(search)

                storage_item['title'] = title
                storage_item['cite'] = cite
                storage_item['text'] = text
                storage_item['search'] = search



                itemproc.process_item(storage_item, self)

        number = response.xpath("//td/b/text()").extract()
        self.log("-----------NUMBER OF PAGE-----")
        self.log(number[0] + "")
        if int(number[0]) < 6:
            res = response.xpath("//td[@class='b'][@style='text-align:left']/a[@class='fl']/@href").extract()

            for url in res:
                self.log("--URL TO FOLLOW--")
                self.log(base_url + url)
                request = Request(base_url + url, callback=self.google_selector)
                request.meta['search'] = search
                yield request
