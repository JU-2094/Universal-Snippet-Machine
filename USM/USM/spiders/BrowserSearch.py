#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Requirements:
        pip install --upgrade google-api-python-client
    Spider to extract the urls and data from a request to google
    usage:
        scrapy crawl googlespider -a file='path_to_queries_file' 

    Notes. In PyCharm, the directories must be marked as sources root

    USM -> Universal Snippet Machine
"""
# Todo: Storage items | find a way to run other threads for googleclient api
# Todo: search module->subprocess
# Todo: Use more browsers, the scientist and yahoo,bing,duckduckgo   ETC.

import scrapy
from scrapy import Selector
from scrapy.http import Request, FormRequest
from googleapi.GoogleClient import GoogleClient


class BrowserSearch(scrapy.Spider):
    name = "browserspider"
    base_url = "https://www.google.com/"
    start_urls = ["https://www.google.com/"]

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
        # for query in self.get_query():
        #     yield FormRequest.from_response(response,
        #                                     formdata={'q':query},
        #                                     callback=self.collect_snippet)
        yield FormRequest.from_response(response,
                                        formdata={'q': '"Jorge Flores Valdéz"'},
                                        callback=self.collect_snippet)

    def collect_snippet(self, response):
        snippets = response.xpath("//div[@class='g']").extract()

        self._create_page(response.body, "-test")

        for snippet in snippets:
            # Todo Create json or fill DB
            self.log("----------------")
            self.log(snippet)

            pass

        number = response.xpath("//td/b/text()").extract()

        # if int(number)<5:
        #     for url in response.xpath("//td[@class='b']/a/@href").extract():
        #          yield Request(self.base_url+url, callback=self.collect_snippet)

    def _create_page(self, body, name):
        file = "web%s.html" % name
        with open(file, 'wb') as f:
            f.write(body)