#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>"

"""
Global Dispatcher for the crawler

It reads the to-be-crawled items from the queue
and start worker to crawl subsequent nested pages

de-duplication will be checked before forking the workers
"""

from utils import TaskQueue
from utils import DeDupeCache
from utils import Logger
from page_crawl import GenericPageCrawler
from page_crawl import Page
from google_crawl import GoogleWebCrawler
from settings import Settings

class Dispatcher(object):
  ''' nested crawl dispatcher '''

  def __init__(self, queue, cache, st):
    self.queue = queue
    self.cache = cache
    self.keywords = st.args.keywords
    self.args = st.args

    self.logger = Logger('/tmp/crawl.log')

    self.num_of_pages = 0
    self.bytes_of_pages = 0

    self.max_num_pages = st.args.num

    self.run()

  def bulk_url_enqueue(self, urls):
    for url in urls:
      page = Page(url, 1, 9)
      self.queue.en_queue(page)
    
  def run(self):

    # crawl google web search engine
    gs = GoogleWebCrawler(self.keywords, self.args.fake)

    urls = gs.query()
    self.bulk_url_enqueue(urls)

    while True:
      # get one item from the queue
      # check duplication
      # initialize a generic crawler instance
      # run that instance asyncly
      page = self.queue.de_queue()
      if page:
        print page.url
        GenericPageCrawler(page, self.queue, self.cache, self.keywords, self.args.fake)
        self.num_of_pages += 1
        self.logger.log(page)

      if self.num_of_pages == self.max_num_pages:
        break

    self.logger.close()

