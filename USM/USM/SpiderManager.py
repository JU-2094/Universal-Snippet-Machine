#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

__author__ = "Josué Fabricio Urbina González"

process = CrawlerProcess(get_project_settings())

# Spiders to be executed
# process.crawl("GoogleSearch",file="")
process.crawl("googlespider")
process.crawl("bingspider")
process.start()
