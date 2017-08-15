#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

__author__ = "Josué Fabricio Urbina González"

# todo fix the problems detected, with some of the span and ...
"""
Problems
    -Google Spider
        -In the url, has
            <cite class="kv">
            /.../
            .../
        -text
            <span class="f">
            <span class="nobr">
            
    Pipeline
        -in the writing of the file, the text per line is not correct in some cases
        'cause of commas or other signs.
"""


def get_snippets(id, query):
    process = CrawlerProcess(get_project_settings())

    source = [id, query, "1"]

    process.crawl("googlespider", source=source)
    process.crawl("bingspider", source=source)
    # process.crawl("duckspider", source=source)
    # process.crawl("citespider", source=source)

    process.start()




