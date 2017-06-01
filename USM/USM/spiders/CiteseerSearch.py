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
from USM.learntools.BasicTool import Utils

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
        if self.file != "":
            for search in Utils.get_query(Utils(), file=self.file):
                request = FormRequest.from_response(response,
                                                    formdata={'q': search[1]},
                                                    callback=self.cite_selector)
                request.meta['search'] = search[0]
                yield request

    def cite_selector(self, response):
        Utils.create_page(Utils(), response.body, "-citeseerx")

        base_url = "http://citeseerx.ist.psu.edu/"
        snippets = response.xpath("//div[@class='result']").extract()
        itemproc = self.crawler.engine.scraper.itemproc

        search = response.meta['search']

        for snippet in snippets:
            storage_item = UsmItem()

            title = Selector(text=snippet).xpath("//h3/a/node()").extract()
            # tmpTitle = Selector(text=snippet).xpath("//div[@class='pubinfo']")
            cite = Selector(text=snippet).xpath("//h3/a/@href").extract()
            text = Selector(text=snippet).xpath("//div[@class='snippet']/text()").extract()

            if title.__len__() > 0:
                tmp = ""
                for txt in title:
                    for r in ['<em>', '</em>', '\n']:
                        txt = txt.replace(r, '')
                    tmp = tmp + txt
                title = tmp.strip()
            else:
                title = ""

            if cite.__len__() > 0:
                #Todo check the url
                cite = base_url + cite[0]
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
                self.log("----------QUERY----------------")
                self.log(search)

                storage_item['title'] = title
                storage_item['cite'] = cite
                storage_item['text'] = text
                storage_item['search'] = search

                itemproc.process_item(storage_item, self)

        num = response.xpath("//div[@id='result_info']/strong/text()").extract()

        self.log("----------NUM OF ELEMENTS---------")
        self.log(num[0].split(' ')[2])
        num = num[0].split(' ')[2]

        if int(num) < 60:
            url = response.xpath("//div[@id='result_info']"
                                 "/div[@id='pager']/a/@href").extract()
            self.log("------------URL TO FOLLOW ------------")
            if url.__len__() > 0:
                self.log(base_url + url[0])

                request = Request(base_url+url[0],callback=self.cite_selector)
                request.meta['search'] = search
                yield request
