#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Spider to extract the urls and data from different browsers
    usage:
        scrapy crawl browserspider -a file='path_to_queries_file' 

    Notes. In PyCharm, the directories must be marked as sources root
    In duckduckgo the queries with "querie" doesn't seem to work

    USM -> Universal Snippet Machine
"""
# Todo: Storage items | find a way to run other threads for googleclient api
# Todo: search module->subprocess
# Todo: Create json or fill DB
# Todo: Check the ... in the cites and the complete url in google snippets
# Todo: Automatize bing,duckduckgo and cite links to follow
# Todo: Special Spider for https://academic.microsoft.com/ and http://www.sciencedirect.com/

__author__ = "Josué Fabricio Urbina González"

import scrapy
import re, json
from scrapy import Selector
from scrapy.http import Request, FormRequest
from USM.CustomSearch import GoogleClient
from USM.Buscador import NameParser
from USM.items import UsmItem


class BrowserSearch(scrapy.Spider):
    name = "browserspider"

    # start_urls = ["https://www.google.com.mx/",
    #               "https://duckduckgo.com/"] #,
    #               "https://www.bing.com/",
    #   #Academic Search Engines
    #               "http://citeseerx.ist.psu.edu/" ]
    start_urls = ["https://www.bing.com/"]
    dict_url = {"https://www.google.com.mx/": 1, "https://duckduckgo.com/": 2,
                "https://www.bing.com/": 3, "http://citeseerx.ist.psu.edu/": 4}
    base_url = ""

    def __init__(self, file=None, *args, **kwargs):
        super(BrowserSearch, self).__init__(*args, **kwargs)
        if file is not None:
            self.file = file
        else:
            self.file = ""

    def get_query(self):
        with open(self.file, 'r') as f:
            for line in f:
                yield line

    def parse(self, response):
        #Todo Use DB..? or other method for the queries
        # for query in self.get_query():
        #     yield FormRequest.from_response(response,
        #                                     formdata={'q':query},
        #                                     callback=self.collect_snippet)
        res = response.url.split('/')
        self.base_url = res[0]+"//"+res[2]+"/"

        yield FormRequest.from_response(response,
                                        formdata={'q': 'Jorge Flores'},
                                        callback=self.collect_snippet)

    def collect_snippet(self, response):

        self.log("---------BASE URL---------------")
        self.log(self.base_url)
        if self.dict_url.get(self.base_url, -1) == 1:
            yield self.google_selector(response)
        elif self.dict_url.get(self.base_url, -1) == 2:
            yield self.duck_selector(response)
        elif self.dict_url.get(self.base_url, -1) == 3:
            yield self.bing_selector(response)
        elif self.dict_url.get(self.base_url, -1) == 4:
            yield self.cite_selector(response)

    def google_selector(self, response):
        snippets = response.xpath("//div[@class='g']").extract()
        itemproc = self.crawler.engine.scraper.itemproc


        for snippet in snippets:
            storage_item = UsmItem()

            title = Selector(text=snippet).xpath("//a/b/text() | //a/text()").extract()
            cite = Selector(text=snippet).xpath("//cite").extract()
            text = Selector(text=snippet).xpath("//span[@class='st']").extract()

            if title.__len__() >= 2:
                title = title[0]+title[1]
            else:
                title=""

            if cite.__len__() > 0:
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

                storage_item['title'] = title
                storage_item['cite'] = cite
                storage_item['text'] = text

                itemproc.process_item(storage_item, self)

        number = response.xpath("//td/b/text()").extract()
        self.log("-----------NUMBER OF PAGE-----")
        self.log(number[0] + "")
        if int(number[0]) < 6:
            res = response.xpath("//td[@class='b'][@style='text-align:left']/a[@class='fl']/@href").extract()
            self.log(res)
            for url in res:
                self.log("--URL TO FOLLOW--")
                self.log(self.base_url + url)
                return Request(self.base_url + url, callback=self.collect_snippet)

    def bing_selector(self, response):
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

    def duck_selector(self, response):
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

    def cite_selector(self, response):
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

    def create_page(self, body, name):
        file = "web%s.html" % name
        with open(file, 'wb') as f:
            f.write(body)