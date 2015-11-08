# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import json

class ImagecrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class DeduplicatePipeline(object):
    def __init__(self):
        self.url_seen = set()
        self.file = open('url_set.json','wb')

    def process_item(self, item, spider):
        if item['image_url'] in self.url_seen:
            raise DropItem("Duplicate item found %s" % item)
        else:
            self.url_seen.add(item['image_url'])
        return item

    def close_spider(self,spider):
        for url in self.url_seen:
          line = "\'" + url+ "\' "
          self.file.write(line)
        self.file.close()

class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('items.json','wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item 

    def close_spider(self,spider):
        self.file.close()
