# -*- coding: utf-8 -*-

# Usage: scrapy crawl imageCrawler -a keywords=<love>

import scrapy
import os
import re

from scrapy.http import Request
import imageCrawler.settings
from imageCrawler.items import ImageItem

class imageCrawlerSpider(scrapy.Spider):

  name = "google_text"
  #allowed_domains = ["google.com"]
  keywords = ""

  MAX_IMAGES_PER_QUERY = 200
  PHANTOMJS_SCRIPT = 'js/crawl_goog.js'

  def __init__(self, keywords=None, *args, **kwargs):
    super(imageCrawlerSpider, self).__init__(*args, **kwargs)

    self._script = self._phantomjs_script()
    self.query = keywords

    #url = 'https://www.google.com/' + 'search?' + 'site=imghp' + '&' + 'tbm=isch' + '&' + 'q=%s' % self.query
    #self.start_urls = [url]

  def _phantomjs_script(self):
    # Crawl dir is 3 levels above the current file

    pathfrags = [os.path.dirname(os.path.realpath(__file__))]
    pathfrags.extend(['..'] *  2)
    pathfrags.append(self.PHANTOMJS_SCRIPT)
    return os.path.join(*pathfrags)

  def start_requests(self):
    """ send PhantomJS query with the query keyword """

    meta = {
      'query': self.query,
      'num': self.MAX_IMAGES_PER_QUERY,
      'script': self._script
    }

    #url = 'https://www.google.com/' + 'search?' + 'site=imghp' + '&' + 'tbm=isch' + '&' + 'q=%s' % self.query
    fake_phantonjs_query_url = 'phantomjs://%s' % self.query
    yield Request(fake_phantonjs_query_url, callback=self.parse_phantomjs_response, meta=meta)

  def parse_phantomjs_response(self, response):
    """ parse phantomjs response """
    print 'xxx'
    print response.url
    print 'xxx'
    print response.body

