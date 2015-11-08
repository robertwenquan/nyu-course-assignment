# -*- coding: utf-8 -*-
import scrapy
import os
import re

from scrapy.http import Request
#from crawler.items import ImageItem
import imageCrawler.settings
from imageCrawler.items import ImageItem

class imageCrawlerSpider(scrapy.Spider):
  name = "imageCrawler"
  allowed_domains = ["google.com"]
  start_urls = (
    'https://www.google.com/' + 'search?' + 'site=imghp' + '&' + 'tbm=isch' + '&' + 'q=love',
  )

  def parse(self, response):
    sel = response.selector
    url_list = sel.xpath('//img/@src').extract()

    for url in url_list:
      item = ImageItem()
      item['image_url'] = url
