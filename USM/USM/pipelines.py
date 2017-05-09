# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
#Todo remake the json or add to DB


class UsmPipeline(object):

    def __init__(self):
        #Todo create hashSet for duplicates
        #raise DropItem("Duplicate item found: %s" % item)
        pass

    def open_spider(self, spider):
        self.file = open('items', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
