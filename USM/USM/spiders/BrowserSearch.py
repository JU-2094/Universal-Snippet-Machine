#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Requirements:
        pip install --upgrade google-api-python-client
    Spider to extract the urls and data from a request to google
    usage:
        scrapy crawl browserspider -a file='path_to_queries_file' 

    Notes. In PyCharm, the directories must be marked as sources root
    In duckduckgo the queries with "querie" doesn't seem to work

    USM -> Universal Snippet Machine
"""
# Todo: Storage items | find a way to run other threads for googleclient api
# Todo: search module->subprocess
# Todo Create json or fill DB
# Todo: Check the ... in the cites and the
# Todo: Special Spider for https://academic.microsoft.com/ and http://www.sciencedirect.com/

import scrapy
import re
from scrapy import Selector
from scrapy.http import Request, FormRequest
#from googleapi.GoogleClient import GoogleClient


class BrowserSearch(scrapy.Spider):
    name = "browserspider"

    # start_urls = ["https://www.google.com.mx/",
    #               "https://duckduckgo.com/",
    #               "https://www.bing.com/",
    #   #Academic Search Engines
    #               "http://citeseerx.ist.psu.edu/" ]
    start_urls = ["https://www.google.com/"]
    dict_url = {"https://www.google.com.mx/":1,"https://duckduckgo.com/":2,
                "https://www.bing.com/":3,"http://citeseerx.ist.psu.edu/":4}
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
        #Todo Use DB..? or other method
        # for query in self.get_query():
        #     yield FormRequest.from_response(response,
        #                                     formdata={'q':query},
        #                                     callback=self.collect_snippet)
        res = response.url.split('/')
        self.base_url = res[0]+"//"+res[2]+"/"

        yield FormRequest.from_response(response,
                                        formdata={'q': 'Jorge+Flores'},
                                        callback=self.collect_snippet)

    def collect_snippet(self, response):
        self.log("---------BASE URL---------------")
        self.log(self.base_url)
        if self.dict_url.get(self.base_url,-1)==1:
            self.log("BEGIN PAGE")
            yield self.google_selector(response)

    def google_selector(self,response):
        snippets = response.xpath("//div[@class='g']").extract()

        for snippet in snippets:
            title = Selector(text=snippet).xpath("//a/b/text() | //a/text()").extract()
            cite = Selector(text=snippet).xpath("//cite").extract()
            text = Selector(text=snippet).xpath("//span[@class='st']").extract()

            if title.__len__()>=2:
                title = title[0]+title[1]
            else:
                title=""

            if cite.__len__()>0:
                cite = cite[0]
                for r in ['<cite>','</cite>','<b>','</b>']:
                    cite = cite.replace(r,'')
            else:
                cite=""

            if text.__len__()>0:
                text = text[0]
                for r in ['<span class="st">','</span>','<br>','</br>','<b>','</b>']:
                    text = text.replace(r,'')
            else:
                text=""


            if cite!="":
                self.log("----------------TITLE-----------")
                self.log(title)
                self.log("-------------CITE--------------")
                self.log(cite)
                self.log("-------------TEXT--------------")
                self.log(text)

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

    def create_page(self, body, name):
        file = "web%s.html" % name
        with open(file, 'wb') as f:
            f.write(body)