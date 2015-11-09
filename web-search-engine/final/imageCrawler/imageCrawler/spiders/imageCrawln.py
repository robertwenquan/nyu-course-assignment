# -*- coding: utf-8 -*-

# Usage: scrapy crawl imageCrawler -a keywords=<love>

import scrapy
import os
import re

from scrapy.http import Request
#from crawler.items import ImageItem
import imageCrawler.settings
from imageCrawler.items import ImageItem

class imageCrawlerSpider(scrapy.Spider):
  name = "imageCrawler"

  def __init__(self, keywords=None, *args, **kwargs):
    super(imageCrawlerSpider, self).__init__(*args, **kwargs)
    url = 'https://www.google.com/' + 'search?' + 'site=imghp' + '&' + 'tbm=isch' + '&' + 'q=%s' % keywords
    self.start_urls = []
    self.start_urls.append(url)

  allowed_domains = ["google.com"]

  def parse(self, response):
    sel = response.selector
    url_list = sel.xpath('//img/@src').extract()

    for url in url_list:
      item = ImageItem()
      item['image_url'] = url
      yield item
