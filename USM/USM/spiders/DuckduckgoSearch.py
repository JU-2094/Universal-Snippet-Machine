#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    USM -> Universal Snippet Machine

    Spider to extract data from google
    usage:
        scrapy crawl bingspider -a source=<"query"|"file_json">
    
    Note. Only 1 page can be retrieved successfully
"""
import scrapy
from scrapy.http import FormRequest
from scrapy import Selector
from USM.items import UsmItem
from USM.learntools.BasicTool import Utils

__author__ = "Josué Fabricio Urbina González"


class DuckSearch(scrapy.Spider):
    name = "duckspider"
    start_urls = ["https://duckduckgo.com/"]

    def __init__(self, source=None, *args, **kwargs):
        super(DuckSearch, self).__init__(*args, **kwargs)
        if source is not None:
            self.source = source
        else:
            self.source = ""

    def parse(self, response):
        if self.source != "":
            for search in Utils.get_query(Utils(), query=self.source):
                request = FormRequest.from_response(response,
                                                    formdata={'q': search[2]},
                                                    callback=self.duck_selector)
                request.meta['id_person'] = search[0]
                request.meta['attr'] = search[1]
                request.meta['search'] = search[2]
                yield request

    def duck_selector(self, response):

        base_url = "https://duckduckgo.com/"
        snippets = response\
            .xpath("//div[@class='result results_links results_links_deep web-result ']")\
            .extract()

        itemproc = self.crawler.engine.scraper.itemproc

        id_person = response.meta['id_person']
        base_attr = response.meta['attr']
        search = response.meta['search']

        for snippet in snippets:
            storage_item = UsmItem()

            title = Selector(text=snippet).xpath("//div/h2/a/node()").extract()
            cite = Selector(text=snippet).xpath("//div/a/@href").extract()
            text = Selector(text=snippet).xpath("//div/a[@class='result__snippet']/node()").extract()


            if title.__len__()>0:
                tmp = ""
                for text in title:
                    for r in ["<b>", "</b>"]:
                        text = text.replace(r,'')
                    tmp = tmp + text
                title = tmp
            else:
                title = ""

            if cite.__len__()>0:
                cite = cite[0]
            else:
                cite=""

            if text.__len__()>0:
                tmp = ""
                for txt in title:
                    for r in ["<b>", "</b>"]:
                        txt = txt.replace(r, '')
                    tmp = tmp + txt
                text = tmp
            else:
                text = ""

            if cite != "":
                self.log("---------------------------------")
                self.log("------------TITLE----------------")
                self.log(title)
                self.log("------------CITE-----------------")
                self.log(cite)
                self.log("------------TEXT-----------------")
                self.log(text)
                self.log("-----------ID PERSON-----------------")
                self.log(id_person)
                self.log("-----------SEARCH----------------")
                self.log(search)
                self.log("--------------ATTR---------------")
                self.log(base_attr)

                storage_item['title'] = title
                storage_item['cite'] = cite
                storage_item['text'] = text
                storage_item['id_person'] = id_person
                storage_item['search'] = search
                storage_item['attr'] = base_attr


                itemproc.process_item(storage_item, self)

        # value = response.xpath("//div[@class='nav-link']/form/input[@name='s']/@value").extract()
        # self.log("----------TOTAL COLLECTED DUCK----------")
        # self.log(value[0])
        #
        # if (int(value[0])) < 31:
        #     res = response.xpath("//div[@class='nav-link']/form/input[@name='nextParams']/@value").extract()
        #
        #     for url in res:
        #         self.log("----URL TO FOLLOW----")
        #         self.log(base_url + url)
        #         yield Request(base_url+url,callback=self.duck_selector)
